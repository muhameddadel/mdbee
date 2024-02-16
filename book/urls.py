from django.urls import path
from .views import *

app_name = 'book'

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),

    path('borrowrecords/', borrowrecord_list, name='borrowrecord_list'),
    path('borrowrecords/<int:pk>/', borrowrecord_detail, name='borrowrecord_detail'),
    path('borrowrecords/filter/', borrowrecord_filter, name='borrowrecord_filter'),

    path('books/<int:book_id>/borrow/<int:user_id>/', borrow_book, name='borrow_book'),
    path('borrowrecords/<int:borrow_record_id>/return/', return_book, name='return_book'),
]
