from django.urls import path
from . import views


app_name = 'dds'

urlpatterns = [
    path('api/subcategories/', views.get_subcategories, name='admin_get_subcategories'),
]
