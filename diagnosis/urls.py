from django.urls import path
from . import views

app_name = 'diagnosis'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('diagnose/<slug:slug>/', views.diagnose, name='diagnose'),
    path('result/<int:pk>/', views.result, name='result'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
]
