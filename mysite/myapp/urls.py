from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('energy/<int:customer_id>/<str:smart_meter_msn>', views.energy, name='energy'),
    path('analytics/<int:customer_id>/<str:smart_meter_msn>', views.analytics, name='analytics'),


]