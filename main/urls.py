from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

from . import views
from .forms import CustomLoginForm


app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('works_and_products/', views.stone_works_and_products, name='works_and_products'),
    path('articles/', views.articles, name='articles'),
    path('catalog/filter/', views.filter_products, name='filter_products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    #Аунтификация
    path('login/', auth_views.LoginView.as_view(
        template_name='main/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:home'), name='logout'),
    
    #Регистрация
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    #обработка заказа
    path('create-order/', views.create_order, name='create_order'),
    path('update-order-phone/', views.update_order_phone, name='update_order_phone'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)