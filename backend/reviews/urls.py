from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile, name='profile'),
]
