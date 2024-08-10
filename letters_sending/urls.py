from django.urls import path

from letters_sending.views import AttemptListView
from letters_sending.views.client import *
from letters_sending.views.letters_sending import *
from letters_sending.views.message import *
from letters_sending.views.views import index_page

urlpatterns = [
    # letters_sending
    path('', index_page, name='index'),
    path('letter-sending/', LettersSendingListView.as_view(), name='letter_sending_list'),
    path('letter-sending/detail/<int:pk>', LettersSendingDetailView.as_view(), name='letter_sending_detail'),
    path('letter-sending/create', LettersSendingCreateView.as_view(), name='letter_sending_create'),
    path('letter-sending/edit/<int:pk>', LettersSendingUpdateView.as_view(), name='letter_sending_edit'),
    path('letter-sending/delete/<int:pk>', LettersSendingDeleteView.as_view(), name='letter_sending_delete'),
    # статистика
    path('stat/', AttemptListView.as_view(), name='letter_sending_stat'),

    # message
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('message/edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/create', ClientCreateView.as_view(), name='client_create'),
    path('client/edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

    # отключить рассылку
    path('deactivate-sending/', deactivate_letterssending, name='deactivate-sending'),
]
