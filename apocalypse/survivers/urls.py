from django.urls import path
from survivers import views

urlpatterns = [
    path('api/survivers/', views.survivers_list),
    path('api/survivers/create', views.survivers_create),
    path('api/survivers/update_location/<int:pk>/', views.surviver_update_location),

]