from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *
# Register your models here.
admin.site.register(Screen)
admin.site.register(Show)
# admin.site.register(rating)
# admin.site.register(Certificate)
admin.site.register(Seat)
admin.site.register(User)
admin.site.register(PromoCode)
admin.site.register(PromoCodeUsage)

admin.site.register(Booking)

admin.site.register(Movie)

# class CustomAdminSite(AdminSite):
#     site_header = 'Cinema++'

admin.site.site_header = 'Cinema++ Admin'

# # Create an instance of the custom AdminSite
# custom_admin_site = CustomAdminSite(name='customadmin')

# # Register your models with the custom AdminSite
# custom_admin_site.register(YourModel)

# # Use the custom AdminSite instance instead of the default admin site
# admin.site = custom_admin_site

