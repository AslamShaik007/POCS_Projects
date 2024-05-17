from django.contrib import admin

from .models import (gallery, items, 
                     specialoffers, booking_details, 
                     cms, contactUs, testimonial,
                     AllTables, BookTheTable, 
                     all_settings,category,AddToCartItems,
                     items,SubItems,AdminProfile,OrderDetails)

# Register your models here.

admin.site.register(gallery)

admin.site.register(items)

admin.site.register(specialoffers)

admin.site.register(booking_details)

admin.site.register(cms)

admin.site.register(contactUs)

admin.site.register(testimonial)

admin.site.register(AllTables)

admin.site.register(BookTheTable)

admin.site.register(all_settings)

admin.site.register(category)

admin.site.register(SubItems)

admin.site.register(AdminProfile)

admin.site.register(OrderDetails)

admin.site.register(AddToCartItems)