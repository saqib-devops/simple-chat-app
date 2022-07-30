from django.urls import path

from app import consumer

websocket_urlpatterns = [
    path('ws/ac/<str:pk>/', consumer.MyConsumer.as_asgi()),
]
