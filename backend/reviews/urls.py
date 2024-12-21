from django.urls import path
from . import views
from products import views as product_views
from users import views as user_views

app_name = 'reviews'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('products/', product_views.product_list, name='product_list'),
    path('products/<int:product_id>/', product_views.product_detail, name='product_detail'),

    path('product/<int:product_id>/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('product/<int:product_id>/review/<int:review_id>/edit/', views.update_review, name='update_review'),
    
    # Include user-related URLs
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/', user_views.profile, name='profile'),

]