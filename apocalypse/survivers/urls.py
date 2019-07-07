from django.urls import path
from survivers import views

urlpatterns = [
    path('api/survivers/', views.survivers_list),
    path('api/survivers/create', views.survivers_create),
    path('api/survivers/update_location/<int:pk>/', views.surviver_update_location),
    path('api/survivers/relate_infected/<int:pk>/', views.relate_infected),
    path('api/survivers/statistics', views.percentage_infected_survivors),
    path('api/survivers/report', views.show_reports),

]