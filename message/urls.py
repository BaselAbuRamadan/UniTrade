from django.urls import path
from . import views
app_name = 'message'

urlpatterns = [
    path('', views.message_list, name='message_list'),
    path('message_send/', views.message_send_message, name='send_message'),
    path('message_unread/', views.message_get_unread_count, name='get_unread_count'),
    path('message_history/', views.message_chat_history, name='chat_history'),
    path('message_marked/', views.message_mark_as_read, name='mark_as_read'),
]


