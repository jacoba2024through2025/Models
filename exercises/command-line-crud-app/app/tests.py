from django.test import TestCase
from app.models import Books
from app import models

def create_items(author, book_name, is_checked_out):
    stored = Books.objects.create(author=author, book_name=book_name, is_checked_out=is_checked_out)
    return stored

class TestBooks(TestCase):
    def test_create_book_info(self):
        
        stored = models.create_items(
            "JK Rowling",
            "Harry Potter",
            False
        )

        
        self.assertIsNotNone(stored.id)  
        self.assertEqual(stored.book_name, "Harry Potter")
        self.assertEqual(stored.author, "JK Rowling")
        self.assertFalse(stored.is_checked_out)  

    def test_create_can_view_all_books(self):
        books_data = [
            {
                "book_name": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "is_checked_out": True,
            },
            {
                "book_name": "Diary of a Wimpy Kid",
                "author": "Jeff Kinney",
                "is_checked_out": False,
            },
            {
                "book_name": "The Outsiders",
                "author": "S.E. Hinton",
                "is_checked_out": True,
            },
        ]

        for book_data in books_data:
            models.create_items(
                book_data["author"],
                book_data["book_name"],
                book_data["is_checked_out"],
            )

        books = models.view_all_books()

        self.assertEqual(len(books), len(books_data))

        # Sort both lists to ensure the order doesn't affect the comparison
        books_data_sorted = sorted(books_data, key=lambda c: c["book_name"])
        books_sorted = sorted(books, key=lambda c: c.book_name)

        # Debug output to check contents
        print("Expected books data:", books_data_sorted)
        print("Book Output:", [(book.book_name, book.author, book.is_checked_out) for book in books_sorted])

        for data, book in zip(books_data_sorted, books_sorted):
            self.assertEqual(data["book_name"], book.book_name)
            self.assertEqual(data["author"], book.author)
            self.assertEqual(data["is_checked_out"], book.is_checked_out)

    def test_can_filter_books(self):
        create_items("The Great Gatsby", "F. Scott Fitzgerald", True)
        create_items("Diary of a Wimpy Kid", "Jeff Kinney", False)
        create_items("The Outsiders", "S.E. Hinton", True)


        checked_out_books = models.filter_books(is_checked_out=True)
        self.assertEqual(checked_out_books.count(), 2)
            
        available_books = models.filter_books(is_checked_out=False)
        self.assertEqual(available_books.count(), 1)

        all_books = models.filter_books()
        self.assertEqual(all_books.count(), 3)
    
    def test_can_filter_by_unique_id(self):
        
        book = create_items("JK Rowling", "Harry Potter", False)

        book_result = models.view_book_by_unique_identifier(book.id)

        self.assertIsNotNone(book_result)
        self.assertEqual(book_result.id, book.id)
        self.assertEqual(book_result.book_name, "Harry Potter")
        self.assertEqual(book_result.author, "JK Rowling")
        self.assertFalse(book_result.is_checked_out)

    def test_can_update_book(self):

        book = create_items("Marie Lu", "Legend", False)

        updated_book = models.update_books(book.id, author="Marie L.", book_name="Legend", is_checked_out=True)

        self.assertIsNotNone(updated_book)
        self.assertEqual(updated_book.author, "Marie L.")
        self.assertEqual(updated_book.book_name, "Legend")
        self.assertEqual(updated_book.is_checked_out, True)

    def test_can_delete_book(self):
        book = create_items("Author", "Book Name", False)
        self.assertTrue(models.delete_books(book.id))
        self.assertIsNone(models.view_book_by_unique_identifier(book.id))