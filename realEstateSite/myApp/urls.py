from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home_new, name='Home_new'),
    path('home/', views.home, name='home'),
    path('user_type/', views.user_type, name='user_type'),
    path('customer/register/', views.customer_register, name='customer_register'),
    path('professional/register/', views.professional_register, name='professional_register'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('professional/login/', views.professional_login, name='professional_login'),
    path('customer/home/', views.customer_home, name='customer_home'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/detail/', views.job_detail, name='job_details'),
    path('professional/home/', views.professional_home, name='professional_home'),
    path('professional/get_detail_professional/', views.get_detail_professional, name='get_detail_professional'),
    path('job/choose_pro/', views.choose_pro, name='choose_pro'),
    path('professional/job_offers/', views.job_offers, name='job_offers'),
    path('job/rate_professionals/', views.rate_professionals, name='rate_professionals'),
    path('view_contract/<int:professional_id>/<int:job_detail_id>/', views.view_contract, name='view_contract'),
]



