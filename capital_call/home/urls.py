from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_home, name='index_home'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('new_call', views.new_call, name='new_call'),
    path('summary', views.summary, name='summary'),
    path('reset_data', views.reset_data, name='reset_data'),

]
