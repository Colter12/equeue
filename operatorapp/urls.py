from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='operator_login'),
    path('dashboard/', views.operator_dashboard, name='operator_dashboard'),
    path('call/<int:ticket_id>/', views.call_ticket, name='call_ticket'),
    path('start/<int:ticket_id>/', views.start_service, name='start_service'),
    path('finish/<int:ticket_id>/', views.finish_service, name='finish_service'),
    path('redirect/<int:ticket_id>/', views.redirect_ticket, name='redirect_ticket'),
    path('operator/cancel/<int:ticket_id>/', views.cancel_service, name='cancel_service'),
]
