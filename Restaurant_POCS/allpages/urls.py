from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from allpages import api_views

urlpatterns = [
    path('menu_details/', api_views.GetMenuItemsAndSubItemsAPIView.as_view(), name = 'menu_details'),
    path('user_book_table/', api_views.UserTableBookingAPIView.as_view(), name = 'user_book_table'),
    path('add_item_subitem/', api_views.AddItemWithSubitemAPIView.as_view(), name = 'add_item_subitem'),
    path('admin_details/', api_views.AddItemWithSubitemAPIView.as_view(), name = 'admin_details'),
    path('add_cart/', api_views.AddToCartAPIView.as_view(), name = 'add_cart'),
    path('checkout/order/', api_views.CheckoutAPIView.as_view(), name = 'check_out'),
    
]