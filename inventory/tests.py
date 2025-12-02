from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Asset, Category

User = get_user_model()

class AssetFlowTests(APITestCase):
    def setUp(self):
        # 1. Setup the "World" (Admin, Employee, Category, Asset)
        self.admin = User.objects.create_superuser(email='admin@test.com', password='password123')
        self.employee = User.objects.create_user(email='employee@test.com', password='password123')
        
        self.category = Category.objects.create(name="Test Electronics")
        self.asset = Asset.objects.create(
            name="Test Laptop", 
            serial_number="12345", 
            category=self.category,
            status=Asset.Status.AVAILABLE
        )
        
        # 2. Get the Token (Login as Admin)
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'admin@test.com', 'password': 'password123'}, format='json')
        self.token = response.data['access']
        
        # 3. Attach Token to all future requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_checkout_flow(self):
        """
        Test the full story: Checkout -> Verify Status -> Return -> Verify Status
        """
        # A. Try to Checkout
        url = reverse('asset-checkout', args=[self.asset.id])
        data = {'employee_id': self.employee.id}
        response = self.client.post(url, data, format='json')

        # Check: Did it succeed?
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check: Did DB update?
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.status, 'ASSIGNED')
        self.assertEqual(self.asset.assigned_to, self.employee)

        # B. Try to Return
        url = reverse('asset-return-asset', args=[self.asset.id]) # Note: DRF adds '_asset' to custom action names sometimes
        response = self.client.post(url, format='json')

        # Check: Did it succeed?
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check: Is it Available again?
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.status, 'AVAILABLE')
        self.assertIsNone(self.asset.assigned_to)

    def test_security_lock(self):
        """
        Test that an unauthenticated user cannot see assets
        """
        self.client.credentials() # Clear the token
        url = reverse('asset-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)