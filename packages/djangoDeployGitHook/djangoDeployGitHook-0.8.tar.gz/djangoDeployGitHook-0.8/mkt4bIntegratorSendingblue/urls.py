
from django.urls import path

from mkt4bIntegratorSendingblue import views

urlpatterns = [
    path('list_campaign', views.list_campaign, name='list_campaign'),
    path('campaign_detail/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('create_campaign', views.create_campaign, name='create_campaign'),
]
