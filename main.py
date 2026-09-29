import json
import os


# -------------------- BOOK CLASS --------------------

class Book:
    def __init__(self, book_id, title, author, issued=False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["issued"]
        )


# -------------------- LIBRARY CLASS --------------------

class Library:

    def __init__(self, filename="books.json"):
        self.filename = filename

        # Dictionary works like a HashMap
        # book_id -> Book object
        self.books = {}

        self.load_data()

    # ---------- SAVE DATA ----------

    def save_data(self):
        data = {}

        for book_id, book in self.books.items():
            data[book_id] = book.to_dict()

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    # ---------- LOAD DATA ----------

    def load_data(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)

            for book_id, book_data in data.items():
                self.books[book_id] = Book.from_dict(book_data)

        except json.JSONDecodeError:
            print("Error reading books.json")

    # ---------- ADD BOOK ----------

    def add_book(self):
        book_id = input("Enter Book ID: ")

        if book_id in self.books:
            print("Book ID already exists!")
            return

        title = input("Enter Book Title: ")
        author = input("Enter Author Name: ")

        book = Book(book_id, title, author)

        self.books[book_id] = book

        self.save_data()

        print("Book added successfully!")

    # ---------- SEARCH BOOK ----------

    def search_book(self):
        keyword = input("Enter title or author to search: ").lower()

        found = False

        for book in self.books.values():

            if (keyword in book.title.lower() or
                    keyword in book.author.lower()):

                print("\nBook ID :", book.book_id)
                print("Title   :", book.title)
                print("Author  :", book.author)
                print("Status  :", "Issued" if book.issued else "Available")

                found = True

        if not found:
            print("No books found.")

    # ---------- ISSUE BOOK ----------

    def issue_book(self):
        book_id = input("Enter Book ID to issue: ")

        if book_id not in self.books:
            print("Book not found!")
            return

        book = self.books[book_id]

        if book.issued:
            print("Book is already issued!")
            return

        book.issued = True

        self.save_data()

        print("Book issued successfully!")

    # ---------- RETURN BOOK ----------

    def return_book(self):
        book_id = input("Enter Book ID to return: ")

        if book_id not in self.books:
            print("Book not found!")
            return

        book = self.books[book_id]

        if not book.issued:
            print("Book is already available!")
            return

        book.issued = False

        self.save_data()

        print("Book returned successfully!")

    # ---------- DISPLAY ALL BOOKS ----------

    def display_books(self):

        if not self.books:
            print("No books in library.")
            return

        print("\n========== ALL BOOKS ==========")

        for book in self.books.values():

            print("\nBook ID :", book.book_id)
            print("Title   :", book.title)
            print("Author  :", book.author)
            print("Status  :", "Issued" if book.issued else "Available")

    # ---------- REPORT ----------

    def reports(self):

        total_books = len(self.books)

        issued_books = 0

        for book in self.books.values():
            if book.issued:
                issued_books += 1

        available_books = total_books - issued_books

        print("\n========== LIBRARY REPORT ==========")
        print("Total Books     :", total_books)
        print("Issued Books    :", issued_books)
        print("Available Books :", available_books)


# -------------------- MAIN PROGRAM --------------------

def main():

    library = Library()

    while True:

        print("\n================================")
        print("     LIBRARY BOOK MANAGER")
        print("================================")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Display All Books")
        print("6. Library Report")
        print("7. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            library.add_book()

        elif choice == "2":
            library.search_book()

        elif choice == "3":
            library.issue_book()

        elif choice == "4":
            library.return_book()

        elif choice == "5":
            library.display_books()

        elif choice == "6":
            library.reports()

        elif choice == "7":
            print("Thank you for using Library Book Manager!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()