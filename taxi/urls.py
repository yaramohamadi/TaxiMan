"""untitled4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from . import views

urlpatterns = [

    path('driver_signin_click/', views.driver_sign_in_view),
    path('driver_signup_click/', views.driver_sign_up_view),
    path('customer_signin_click/', views.customer_sign_in_view),
    path('customer_signup_click/', views.customer_sign_up_view),
    path('signout/', views.logout_view),

    path('dash/', views.customer_dashboardview),
    path('customer_editprofile/', views.customer_editprofile_view),
    path('customer_fillinyowallet/', views.customer_filinyowallet_view),
    path('customer_newcommonaddress/', views.customer_addcommonaddress_view),
    path('customer_deleteaddress/', views.customer_deletecommonaddress_view),
    path('customer_newtrip/', views.customer_newtrip_view),
    path('customer_deletetrip/', views.customer_deletetrip_view),
    path('customer_scoreyodrivah_click/', views.customer_scoreyodriver_click_view),
    path('customer_scoreyodrivah_submit/', views.customer_scoreyodriver_submit_view),

    path('driver_dash/', views.driver_dashboardview),
    path('driver_editprofile/', views.driver_editprofile_view),
    path('driver_accepttrip/', views.driver_accepttrip_view),
    path('driver_scoreyocustomah/', views.driver_scoreyocustomer_view),

    path('', views.home),
]
