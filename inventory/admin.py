from django.contrib import admin
from .models import Asset,Category
# Register your models here.

admin.site.register(Category)
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=('name','serial_number','category','status','assigned_to')
    list_filter=('status','category')
    search_fields=('name','serial_number')
