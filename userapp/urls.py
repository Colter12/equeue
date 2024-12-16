# userapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.subcategory_list, name='subcategory_list'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
]
