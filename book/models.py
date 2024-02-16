from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()

    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} - Borrowed by {self.borrower.username}"
