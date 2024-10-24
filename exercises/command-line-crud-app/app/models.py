from django.db import models


from django.core.exceptions import ObjectDoesNotExist

class Books(models.Model):
    author = models.CharField(max_length=100)
    book_name = models.CharField(max_length=100)
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book_name} by {self.author}"

#creates our items
def create_items(author, book_name, is_checked_out):
    stored = Books.objects.create(author=author, book_name=book_name, is_checked_out= is_checked_out)
    return stored

#function to view all items at once
def view_all_books():
    return Books.objects.all()

#search for books based on some kind of fiter in our case it's whether its checked out or not
def filter_books(is_checked_out=None):
    if is_checked_out != None:
        return Books.objects.filter(is_checked_out=is_checked_out)
    return Books.objects.all()

#view by some unique identifier
def view_book_by_unique_identifier(bookid):
    try:
        return Books.objects.get(id=bookid)
    except ObjectDoesNotExist:
        return None
#updates books
def update_books(bookid, author=None, book_name=None, is_checked_out=None):
    try:
        book = Books.objects.get(id=bookid)
        if author is not None:
            book.author = author
        if book_name is not None:
            book.book_name = book_name
        if is_checked_out is not None:
            book.is_checked_out = is_checked_out
        book.save()
        return book
    except ObjectDoesNotExist:
        return None

#deletes an individual book
def delete_books(bookid):
    try:
        book = Books.objects.get(id=bookid)
        book.delete()
        return True
    except ObjectDoesNotExist:
        return False
