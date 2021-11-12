from django.urls import path

from . import views

urlpatterns = [
    path('stations/', views.get_all_stations),
    path('stations/lookup', views.get_stations_by_lookup),
    # Refactor to a single "lookup" endoint with query params
    path('stations/line/<str:line>', views.get_stations_on_route),
    path('stations/borough/<str:borough>', views.get_stations_in_borough),
]
