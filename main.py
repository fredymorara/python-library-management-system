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
        """Updates the number of available copies (increase/decrease)."""
        self.available_copies += number

class Member:
    """
    Represents a library member.
    """
    def __init__(self, member_id, name, borrowed_books=None):
        self.member_id = member_id
        self.name = name
        # Initialize borrowed_books as an empty list if not provided
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def borrow_book(self, book_title):
        """Adds a book title to the member's borrowed list."""
        if book_title not in self.borrowed_books:
            self.borrowed_books.append(book_title)

    def return_book(self, book_title):
        """Removes a book title from the member's borrowed list."""
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)

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
    Represents the library, managing books, members, and all transactions.
    """
    def __init__(self):
        self.books = []    # Stores Book objects
        self.members = []  # Stores Member objects
        self.borrow_count = {} # Tracks how many times each book has been borrowed
        self._load_data()  # Private helper method to load all data at startup

    def _load_data(self):
        """Loads all initial data (books, members) from files."""
        self._load_books()
        self._load_members()

    # --- File Handling Methods ---
    def _save_books(self):
        """Saves the current list of books to books.txt."""
        with open("books.txt", "w") as f:
            for book in self.books:
                f.write(f"{book.book_id},{book.title},{book.author},{book.available_copies}\n")

    def _load_books(self):
        """Loads the list of books from books.txt."""
        if not os.path.exists("books.txt"):
            return # No file yet, so no books to load
        with open("books.txt", "r") as f:
            for line in f:
                if line.strip(): # Skip empty lines
                    try:
                        book_id, title, author, copies = line.strip().split(',')
                        self.books.append(Book(book_id, title, author, int(copies)))
                        # Initialize borrow_count for existing books if needed
                        self.borrow_count[title] = self.borrow_count.get(title, 0) # Ensure existing books are in borrow_count
                    except ValueError:
                        print(f"Warning: Skipping malformed book entry: {line.strip()}")

    def _save_members(self):
        """Saves the current list of members to members.txt."""
        with open("members.txt", "w") as f:
            for member in self.members:
                # Join borrowed book titles with a semicolon for storage
                borrowed_books_str = ";".join(member.borrowed_books)
                f.write(f"{member.member_id},{member.name},{borrowed_books_str}\n")

    def _load_members(self):
        """Loads the list of members from members.txt."""
        if not os.path.exists("members.txt"):
            return # No file yet, so no members to load
        with open("members.txt", "r") as f:
            for line in f:
                if line.strip(): # Skip empty lines
                    parts = line.strip().split(',')
                    try:
                        member_id, name = parts[0], parts[1]
                        # Split the borrowed books string back into a list
                        borrowed_books = parts[2].split(';') if len(parts) > 2 and parts[2] else []
                        self.members.append(Member(member_id, name, borrowed_books))
                    except IndexError:
                        print(f"Warning: Skipping malformed member entry: {line.strip()}")

    def _log_transaction(self, message):
        """Logs a transaction message with a timestamp to transactions.log."""
        with open("transactions.log", "a") as f: # 'a' for append mode
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")

    # --- Utility Methods ---
    def find_book_by_title(self, title):
        """Finds a Book object by its title (case-insensitive)."""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_member_by_id(self, member_id):
        """Finds a Member object by their ID (case-insensitive)."""
        for member in self.members:
            if member.member_id.lower() == member_id.lower():
                return member
        return None

    # --- Core Library Management Methods ---
    def add_book(self, book_id, title, author, available_copies):
        """Creates a new Book object and adds it to the library."""
        if self.find_book_by_title(title):
            print(f"Error: Book with title '{title}' already exists.")
            return

        new_book = Book(book_id, title, author, available_copies)
        self.books.append(new_book)
        self._save_books() # Save changes to file
        print("Book added successfully!")

    def add_member(self, member_id, name):
        """Creates a new Member object and adds it to the library."""
        if self.find_member_by_id(member_id):
            print(f"Error: Member with ID '{member_id}' already exists.")
            return

        new_member = Member(member_id, name)
        self.members.append(new_member)
        self._save_members() # Save changes to file
        print("Member added successfully!")

    def display_all_books(self):
        """Displays information for all books in the library."""
        if not self.books:
            print("No books in the library.")
            return
        print("\n--- All Books ---")
        for book in self.books:
            book.display_info()
        print("-----------------")

    def display_all_members(self):
        """Displays information for all members in the library."""
        if not self.members:
            print("No members in the library.")
            return
        print("\n--- All Members ---")
        for member in self.members:
            member.display_member_info()
        print("-------------------")

    def borrow_transaction(self, member_id, book_title):
        """Handles the process of a member borrowing a book."""
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_title(book_title)

        if member is None:
            print(f"Error: Member with ID '{member_id}' not found.")
            return
        if book is None:
            print(f"Error: Book with title '{book_title}' not found.")
            return
        if book.available_copies <= 0:
            print(f"Error: No available copies of '{book_title}'.")
            return
        if book.title in member.borrowed_books:
            print(f"Error: Member '{member.name}' has already borrowed '{book_title}'.")
            return

        book.update_copies(-1) # Decrease available copies
        member.borrow_book(book.title) # Add to member's borrowed list
        self._log_transaction(f"Borrowed: '{book.title}' by {member.name} (ID: {member.member_id})")
        self._save_books() # Save updated book count
        self._save_members() # Save updated member's borrowed list
        print(f"Book '{book.title}' successfully borrowed by {member.name}.")

    def return_transaction(self, member_id, book_title):
        """Handles the process of a member returning a book."""
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_title(book_title)

        if member is None:
            print(f"Error: Member with ID '{member_id}' not found.")
            return
        if book is None:
            print(f"Error: Book with title '{book_title}' not found.")
            return
        if book.title not in member.borrowed_books:
            print(f"Error: Member '{member.name}' did not borrow '{book_title}'.")
            return

        book.update_copies(1) # Increase available copies
        member.return_book(book.title) # Remove from member's borrowed list
        self._log_transaction(f"Returned: '{book.title}' by {member.name} (ID: {member.member_id})")
        self._save_books() # Save updated book count
        self._save_members() # Save updated member's borrowed list
        print(f"Book '{book.title}' successfully returned by {member.name}.")

    # --- Additional Features ---
    def search_by_author(self, author_name):
        """Searches for and displays books by a specific author."""
        found_books = [book for book in self.books if author_name.lower() in book.author.lower()]
        if not found_books:
            print(f"No books found by author '{author_name}'.")
            return
        print(f"\n--- Books by '{author_name}' ---")
        for book in found_books:
            book.display_info()
        print("-------------------------------")

    def most_borrowed_book(self):
        """Analyzes transactions to determine and display the most borrowed book(s)."""
        # We need to re-read transactions.log to get an accurate count
        # as self.borrow_count is only updated on initial load and during borrow_transaction
        current_borrow_counts = {}
        if os.path.exists("transactions.log"):
            with open("transactions.log", "r") as f:
                for line in f:
                    if "Borrowed:" in line:
                        try:
                            # Extract title from log line: "'Title' by Member Name"
                            # This assumes the format: Borrowed: 'BOOK TITLE' by MEMBER NAME (ID: MEMBER_ID)
                            title_start = line.find("'" ) + 1
                            title_end = line.find("'", title_start)
                            if title_start != -1 and title_end != -1:
                                book_title = line[title_start:title_end]
                                current_borrow_counts[book_title] = current_borrow_counts.get(book_title, 0) + 1
                        except Exception as e:
                            print(f"Warning: Could not parse transaction log line: {line.strip()} - {e}")
                            continue

        if not current_borrow_counts:
            print("No borrow transactions recorded yet.")
            return

        max_borrows = max(current_borrow_counts.values())
        most_borrowed = [
            title for title, count in current_borrow_counts.items()
            if count == max_borrows
        ]

        print("\n--- Most Borrowed Book(s) ---")
        for title in most_borrowed:
            print(f"- '{title}' (borrowed {max_borrows} time(s))")
        print("-----------------------------")

    def generate_transaction_report(self):
        """Reads and displays the entire transaction history from transactions.log."""
        if not os.path.exists("transactions.log"):
            print("No transactions have been recorded yet.")
            return
        print("\n===== Transaction History =====")
        with open("transactions.log", "r") as f:
            print(f.read())
        print("===============================")

def main():
    """
    Main function to run the library management system.
    """
    library = Library() # Initialize our Library system

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
        print("9. Transaction History Report")
        print("10. Exit")
        print("===========================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            book_id = input("Enter Book ID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            try:
                available_copies = int(input("Enter Available Copies: "))
                library.add_book(book_id, title, author, available_copies)
            except ValueError:
                print("Invalid input for available copies. Please enter a number.")
        elif choice == '2':
            member_id = input("Enter Member ID: ")
            name = input("Enter Member Name: ")
            library.add_member(member_id, name)
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
            author_name = input("Enter Author's Name to Search: ")
            library.search_by_author(author_name)
        elif choice == '8':
            library.most_borrowed_book()
        elif choice == '9':
            library.generate_transaction_report()
        elif choice == '10':
            print("Exiting the system. Goodbye!")
            break # Exit the loop and end the program
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()