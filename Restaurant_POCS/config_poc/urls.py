"""
URL configuration for config_poc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from allpages import views

from control_panel import views as view

from django.conf import settings  
from django.conf.urls.static import static

urlpatterns = [
    ################ Login Register ##########
    path('register', views.registration, name="register"),
    path('login/', views.login_view, name = "login"),
    path('logout/', views.logout_view, name='logout'),
    path('check-session/', views.check_session_view, name='check_session'),
    
    ##########################################

    path('admin/', admin.site.urls),
    path('restaurant/', include('control_panel.urls')),
    path('allpages/', include('allpages.urls')),
    path('admin-login/', view.Login, name = "admin_login"),
    path('log-out/', view.LogoutUser, name = "admin_logout"),
    # path('', views.index, name="index"),
    path('', views.index_main, name="index"),
    path("subscribe", views.subscribe_user, name= "subscribe_user"),
    path('index-burgers', views.index_burgers, name="index_burgers"),
    path('index-sliders', views.index_sliders, name="index_sliders"),
    path('index-video', views.index_video, name="index_video"),
    path('about', views.about_us, name="about"),
    path('gallery', views.gallery_listing, name="gallery"),
    path('book-a-table', views.book_a_table, name="book_a_table"),
    path('faq', views.faq, name="faq"),
    path('offers', views.offers, name="offers"),
    path('order', views.order, name="order"),
    path('order_category/<int:category_id>/', views.order_category, name= "order_category"),
    path('add_to_cart', views.add_to_cart, name="add_to_cart"),
    path('edit_to_cart', views.edit_to_cart, name="edit_to_cart"),
    path('delete_to_cart', views.delete_to_cart, name="delete_to_cart"),   
    path('view_cart',views.view_cart, name="view_cart"),
    path('my_orders',views.my_orders, name="my_orders"),
    path('checkout', views.checkout, name="checkout"),
    path('reviews', views.reviews, name="reviews"),
    path('services', views.services, name="services"),
    path('contact', views.contact, name="contact"),
    path('thankyou', views.thankyou_page, name="thankyou"),
    path('category_detail/<int:category_id>/', views.category_detail, name='category_detail'),
    
    ############ Add to Cart ###############
    path("edit_cart_details/<int:id>", views.edit_cart_details, name = "edit_cart_details"),
    path("delete_cart_details/<int:id>", views.delete_cart_details, name = "delete_cart_details"),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
