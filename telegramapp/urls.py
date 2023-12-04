from django.urls import path
from .views import MessageView

urlpatterns = [
    path('send_messages/', MessageView.as_view(), name='send_messages'),
]