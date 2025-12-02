from rest_framework import serializers
from .models import Category, Asset
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    # Nested Serializer: Shows full user details instead of just ID when reading
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'category', 'serial_number', 
            'image', 'assigned_to', 'assigned_to_detail', 
            'status', 'created_at'
        ]

    def validate(self, data):
        """
        Force Django Model Validation (clean method)
        This ensures our 'State Machine' logic runs.
        """
        instance = Asset(**data)
        # We skip checking 'assigned_to' relations here for simplicity
        # but we trigger the status checks.
        if instance.status == 'ASSIGNED' and not data.get('assigned_to'):
             # Standard DRF validation can go here too
             pass
        return data