from django.contrib import admin
from .models import profile,PurchaseOrder,VendorProfile
# Register your models here.
admin.site.register(profile)
admin.site.register(PurchaseOrder)
admin.site.register(VendorProfile)
