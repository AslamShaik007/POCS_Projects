from django.contrib import admin
from django.urls import path
from Parser_app import views
from rest_framework import routers


urlpatterns = [
    path('admin-site/', admin.site.urls),
    path('parse-pan/', views.PanCardParser.as_view(), name = 'parse-pan'),
]



router = routers.SimpleRouter()


router.register(r'parse-adhar', views.ParseAdharView, basename="parse-adhar")




urlpatterns += router.urls
