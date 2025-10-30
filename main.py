
import os
import datetime

class Book:
    """
    Represents a book in the library.
    """
    def __init__(self, book_id, title, author, available_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.available_copies = int(available_copies)

    def display_info(self):
        """Displays the book's information."""
        print(f"Book ID: {self.book_id} | Title: {self.title} | Author: {self.author} | Available: {self.available_copies}")

    def update_copies(self, number):
        """Updates the number of available copies."""
        self.available_copies += number

class Member:
    """
    Represents a library member.
    """
    def __init__(self, member_id, name, borrowed_books=None):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def borrow_book(self, book):
        """Adds a book to the member's borrowed list."""
        if book.title not in self.borrowed_books:
            self.borrowed_books.append(book.title)

    def return_book(self, book):
        """Removes a book from the member's borrowed list."""
        if book.title in self.borrowed_books:
            self.borrowed_books.remove(book.title)

    def display_member_info(self):
        """Displays the member's information and borrowed books."""
        print(f"Member ID: {self.member_id} | Name: {self.name}")
        if self.borrowed_books:
            print("  Borrowed Books:")
            for book_title in self.borrowed_books:
                print(f"  - {book_title}")
        else:
            print("  No books currently borrowed.")


class Library:
    """
    Represents the library, managing books, members, and transactions.
    """
    def __init__(self):
        self.books = []
        self.members = []
        self.borrow_count = {}
        self.load_books()
        self.load_members()

    def add_book(self, book):
        """Adds a new book to the library."""
        self.books.append(book)
        self.save_books()
        print("Book added successfully!")

    def add_member(self, member):
        """Adds a new member to the library."""
        self.members.append(member)
        self.save_members()
        print("Member added successfully!")

    def display_all_books(self):
        """Displays all books in the library."""
        if not self.books:
            print("No books in the library.")
            return
        for book in self.books:
            book.display_info()

    def display_all_members(self):
        """Displays all members of the library."""
        if not self.members:
            print("No members in the library.")
            return
        for member in self.members:
            member.display_member_info()

    def find_book_by_title(self, title):
        """Finds a book by its title."""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_member_by_id(self, member_id):
        """Finds a member by their ID."""
        for member in self.members:
            if member.member_id.lower() == member_id.lower():
                return member
        return None

    def borrow_transaction(self, member_id, book_title):
        """Handles the borrowing of a book by a member."""
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_title(book_title)

        if member is None:
            print("Error: Member not found.")
            return
        if book is None:
            print("Error: Book not found.")
            return
        if book.available_copies == 0:
            print("Error: No available copies of this book.")
            return
        if book.title in member.borrowed_books:
            print("Error: Member has already borrowed this book.")
            return

        book.update_copies(-1)
        member.borrow_book(book)
        self.borrow_count[book.title] = self.borrow_count.get(book.title, 0) + 1
        self.log_transaction(f"Borrowed: '{book.title}' by {member.name} ({member.member_id})")
        self.save_books()
        self.save_members()
        print(f"Book '{book.title}' borrowed by {member.name}.")

    def return_transaction(self, member_id, book_title):
        """Handles the returning of a book by a member."""
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_title(book_title)

        if member is None:
            print("Error: Member not found.")
            return
        if book is None:
            print("Error: Book not found.")
            return
        if book.title not in member.borrowed_books:
            print("Error: Member has not borrowed this book.")
            return

        book.update_copies(1)
        member.return_book(book)
        self.log_transaction(f"Returned: '{book.title}' by {member.name} ({member.member_id})")
        self.save_books()
        self.save_members()
        print(f"Book '{book.title}' returned by {member.name}.")

    def save_books(self):
        """Saves the list of books to books.txt."""
        with open("books.txt", "w") as f:
            for book in self.books:
                f.write(f"{book.book_id},{book.title},{book.author},{book.available_copies}\n")

    def load_books(self):
        """Loads the list of books from books.txt."""
        if not os.path.exists("books.txt"):
            return
        with open("books.txt", "r") as f:
            for line in f:
                if line.strip():
                    book_id, title, author, copies = line.strip().split(',')
                    self.books.append(Book(book_id, title, author, int(copies)))
                    self.borrow_count[title] = self.borrow_count.get(title, 0)


    def save_members(self):
        """Saves the list of members to members.txt."""
        with open("members.txt", "w") as f:
            for member in self.members:
                borrowed_books_str = ";".join(member.borrowed_books)
                f.write(f"{member.member_id},{member.name},{borrowed_books_str}\n")

    def load_members(self):
        """Loads the list of members from members.txt."""
        if not os.path.exists("members.txt"):
            return
        with open("members.txt", "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    member_id, name = parts[0], parts[1]
                    borrowed_books = parts[2].split(';') if len(parts) > 2 and parts[2] else []
                    self.members.append(Member(member_id, name, borrowed_books))

    def log_transaction(self, message):
        """Logs a transaction to the transactions.log file."""
        with open("transactions.log", "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")

    def search_by_author(self, author_name):
        """Searches for books by a given author."""
        found_books = [book for book in self.books if author_name.lower() in book.author.lower()]
        if not found_books:
            print(f"No books found by author '{author_name}'.")
            return
        print(f"Books by '{author_name}':")
        for book in found_books:
            book.display_info()

    def most_borrowed_book(self):
        """Displays the most borrowed book(s)."""
        if not self.borrow_count:
            print("No books have been borrowed yet.")
            return
        
        # Load historical borrow counts from transactions.log
        if os.path.exists("transactions.log"):
            with open("transactions.log", "r") as f:
                for line in f:
                    if "Borrowed:" in line:
                        try:
                            title_part = line.split("'")[1]
                            self.borrow_count[title_part] = self.borrow_count.get(title_part, 0) + 1
                        except IndexError:
                            continue # Skip malformed lines

        if not self.borrow_count:
            print("No borrow transactions recorded yet.")
            return

        max_borrows = max(self.borrow_count.values())
        most_borrowed = [title for title, count in self.borrow_count.items() if count == max_borrows]

        print("Most Borrowed Book(s):")
        for title in most_borrowed:
            print(f"- {title} (borrowed {max_borrows} time(s))")


    def generate_transaction_report(self):
        """Displays the entire transaction history from transactions.log."""
        if not os.path.exists("transactions.log"):
            print("No transactions have been recorded yet.")
            return
        print("===== Transaction History =====")
        with open("transactions.log", "r") as f:
            print(f.read())
        print("==============================")


def main():
    """
    Main function to run the library management system.
    """
    library = Library()

    while True:
        print("\n===== SMART LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add New Book")
        print("2. Add New Member")
        print("3. Display All Books")
        print("4. Display All Members")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Search by Author")
        print("8. Most Borrowed Book")
        print("9. Transaction History")
        print("10. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            book_id = input("Enter Book ID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            try:
                available_copies = int(input("Enter Available Copies: "))
                library.add_book(Book(book_id, title, author, available_copies))
            except ValueError:
                print("Invalid input for copies. Please enter a number.")
        elif choice == '2':
            member_id = input("Enter Member ID: ")
            name = input("Enter Name: ")
            library.add_member(Member(member_id, name))
        elif choice == '3':
            library.display_all_books()
        elif choice == '4':
            library.display_all_members()
        elif choice == '5':
            member_id = input("Enter Member ID: ")
            book_title = input("Enter Title of Book to Borrow: ")
            library.borrow_transaction(member_id, book_title)
        elif choice == '6':
            member_id = input("Enter Member ID: ")
            book_title = input("Enter Title of Book to Return: ")
            library.return_transaction(member_id, book_title)
        elif choice == '7':
            author = input("Enter Author's Name: ")
            library.search_by_author(author)
        elif choice == '8':
            library.most_borrowed_book()
        elif choice == '9':
            library.generate_transaction_report()
        elif choice == '10':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
