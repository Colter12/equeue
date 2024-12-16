from django.urls import path
from . import views

urlpatterns = [
    path('', views.statistics_view, name='statistics'),
    path('filter/', views.filter_statistics, name='filter_statistics'),
    path('statistics/filter/', views.filter_statistics, name='filter_statistics'),
]

