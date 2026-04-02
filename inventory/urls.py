from django.urls import path
from . import views

urlpatterns = [
    path('asset/<uuid:asset_id>/broken/',views.mark_broken,name='mark_broken'),
    path('mark-available/<uuid:asset_id>/',views.mark_available,name='mark_available'),
]
