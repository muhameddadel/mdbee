import datetime
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# books CRUD

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])  
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# borrow records CRUD
@api_view(['GET', 'POST'])
def borrowrecord_list(request):
    if request.method == 'GET':
        borrow_records = BorrowRecord.objects.all()
        serializer = BorrowRecordSerializer(borrow_records, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BorrowRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def borrowrecord_detail(request, pk):
    borrow_record = get_object_or_404(BorrowRecord, pk=pk)

    if request.method == 'GET':
        serializer = BorrowRecordSerializer(borrow_record)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BorrowRecordSerializer(borrow_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        borrow_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def borrowrecord_filter(request):
    borrower_id = request.GET.get('borrower_id')
    book_id = request.GET.get('book_id')

    if borrower_id:
        borrow_records = BorrowRecord.objects.filter(borrower=borrower_id)
    elif book_id:
        borrow_records = BorrowRecord.objects.filter(book=book_id)
    else:
        borrow_records = BorrowRecord.objects.all()

    serializer = BorrowRecordSerializer(borrow_records, many=True)
    return Response(serializer.data)

# borrow and return book 
@api_view(['POST'])
def borrow_book(request, book_id, user_id):
    book = get_object_or_404(Book, id=book_id, availability=True)

    if not book.availability:
        return Response({'message': 'The book is not available right now.'}, status=status.HTTP_400_BAD_REQUEST)

    borrower = get_object_or_404(User, id=user_id)

    borrow_record_data = {
        'book': book.id,
        'borrower': borrower.id,
    }

    borrow_record_serializer = BorrowRecordSerializer(data=borrow_record_data)
    if borrow_record_serializer.is_valid():
        borrow_record_serializer.save()

        book.availability = False
        book.save()

        return Response(borrow_record_serializer.data, status=status.HTTP_201_CREATED)

    return Response(borrow_record_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def return_book(request, borrow_record_id):
    borrow_record = get_object_or_404(BorrowRecord, id=borrow_record_id)
    book = borrow_record.book

    book.availability = True
    book.save()

    borrow_record.return_date = datetime.date.today()
    borrow_record.save()

    return Response(status=status.HTTP_200_OK)