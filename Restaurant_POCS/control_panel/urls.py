"""keylogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
# from controlPanel import api_views

urlpatterns = [
    # path('', views.listCategory, name = 'homepage'),
    path('dashboard/', views.listCategory, name = 'dashboard'),
    
    path("admin-profile/", views.AdminProfileDetails, name = "admin_profile"),
    
    path('list-category/', views.listCategory, name = 'list_category'),
    path('add-category/', views.addCategory, name = 'add_category'),
    path('update-category/<int:baseId>/', views.updateCategory, name = 'update_category'),
    path('delete/category/', views.deleteCategory, name = 'delete_category'), 
    
    path('list-order/', views.listOrder, name = 'list_order'),
    path('list-order/details/<int:baseId>/', views.listOrderDetails, name = 'list_order_details'),
    
    path('list-item/', views.listItem, name = 'list_item'),
    path('add-item/', views.addItem, name = 'add_item'),
    path('update-item/<int:baseId>/', views.updateItem, name = 'update_item'),
    path('delete/item/', views.deleteItem, name = 'delete_item'), 
    
    path('list-sub-item/', views.listSubItem, name = 'list_sub_item'),
    path('add-sub-item/', views.addSubItem, name = 'add_sub_item'),
    path('update-sub-item/<int:baseId>/', views.updateSubItem, name = 'update_sub_item'),
    path('delete-subitem/', views.deleteSubItem, name = 'delete_subitem'), 
    
    path('list-gallery/', views.listGallery, name = 'list_gallery'),
    path('add-gallery/', views.addGallery, name = 'add_gallery'),
    path('update-gallery/<int:baseId>/', views.updateGallery, name = 'update_gallery'),
    path('delete/gallery/', views.deleteGallery, name = 'delete_gallery'), 
    
    path('list-content/', views.listContent, name = 'list_content'),
    path('add-content/', views.addContent, name = 'add_content'),
    path('update-content/<int:baseId>/', views.updateContent, name = 'update_content'),
    path('delete/content/', views.deleteContent, name = 'delete_content'), 
    
    path('list-testimonial/', views.listTestimonial, name = 'list_testimonial'),
    path('add-testimonial/', views.addTestimonial, name = 'add_testimonial'),
    path('update-testimonial/<int:baseId>/', views.updateTestimonial, name = 'update_testimonial'),
    path('delete/testimonial/', views.deleteTestimonial, name = 'delete_testimonial'), 
    
    path('list-special/', views.listSpecial, name = 'list_special'),
    path('add-special/', views.addSpecial, name = 'add_special'),
    path('update-special/<int:baseId>/', views.updateSpecial, name = 'update_special'),
    path('delete/special/', views.deleteSpecial, name = 'delete_special'), 
    
    path('list-contactus/', views.listContactUs, name = 'list_contactus'),
    path('update-all-setting/<int:baseId>/', views.updateAllSetting, name = 'update_all_setting'),
    
    ############################################

    path('list-table/', views.ListTablesView, name = 'list_table'),
    path('update-table/<int:baseId>/', views.UpdateTablesView, name = 'update_table'),
    path('create-table/', views.AdminAllTablesAddView, name = 'create_table'),
    path('delete-table/', views.deleteTableView, name = 'delete_table'),

    path('list-booked-tables/', views.BookedTablesListView, name = 'list_booked_tables'),
    path('booke-table/', views.BookTheNewTableView, name = 'booke_table'),
    path('update-booked-table/<int:baseId>/', views.UpdateTheBookedTable, name = 'update_booked_table'),

    ###############################################
    path('updateAdmin/<int:baseId>/', views.updateAdmin, name = 'update_Admin'),
    
    # path('admin_details/', api_views.AddAdminProfile.as_view(), name = 'admin_details'),
    # path("register/",api_views.UserRegistartionAPIView.as_view(),name = "restartion"),
    # path('create/table/', api_views.AdminAllTablesAddAPIView.as_view(), name = 'create_table'),
    # path('book/table/', api_views.UserTableBookingAPIView.as_view(), name = 'book_table'),
    # path('add-item-subitems/', api_views.AddItemWithSubitemAPIView.as_view(), name = 'add_item_subitems'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)