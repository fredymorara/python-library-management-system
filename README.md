# 📚 Smart Library Management System

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Code Style: PEP 8](https://img.shields.io/badge/code%20style-pep8-orange.svg)

A menu-driven command-line application for managing books, members, and library transactions, built with Object-Oriented principles in Python.

---

## ✨ Features

-   **Book Management**: Add new books and view the complete library catalog.
-   **Member Management**: Register new members and see a list of all registered members.
-   **Transaction Handling**: Process book borrowing and returns with error checking.
-   **Persistent Storage**: All book and member data is saved to local text files, so data is never lost.
-   **Reporting**:
    -   Generate a complete, timestamped transaction history.
    -   Track and display the most borrowed books.
    -   Search the library catalog by author.

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

-   You must have [Python 3.x](https://www.python.org/downloads/) installed on your system.

### Installation & Execution

1.  **Clone the repository (or download the files):**
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

2.  **(Optional but Recommended) Create and activate a virtual environment:**
    This keeps your project dependencies isolated.
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate the environment
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```
    The interactive menu will appear in your terminal. Follow the on-screen prompts to use the system.

---

## ⚙️ Implementation Walkthrough

This section details the internal structure and logic of the application.

### Project Structure

The project is contained within a single directory with the following key files:

-   `main.py`: The main source file containing all Python code.
-   `books.txt`: The database file for book records.
-   `members.txt`: The database file for member records.
-   `transactions.log`: A running log of all borrow/return activities.

### Core Classes

The application is built around three main classes that model the library's components.

#### `Book` Class
Represents a single book. It stores book-specific data and has methods for displaying its information.
```python
class Book:
    def __init__(self, book_id, title, author, available_copies):
        # ...
```

#### `Member` Class
Represents a library member. It holds member data and tracks the books they have borrowed.
```python
class Member:
    def __init__(self, member_id, name, borrowed_books=None):
        # ...
```

#### `Library` Class
This is the main controller class. It manages the collections of books and members and orchestrates all major operations like transactions and file I/O.
```python
class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.borrow_count = {}
        self.load_books()
        self.load_members()
```

### Data Persistence

-   **Book and Member Data**: When a book or member is added or updated, the entire list of objects is rewritten to `books.txt` or `members.txt` in a comma-separated value (CSV) format. This ensures data integrity between sessions.
-   **Transaction Logging**: The `transactions.log` file is opened in **append mode**, so every new transaction is added to the end of the file without overwriting previous logs.

### Main Execution Logic

-   The script's entry point is the `if __name__ == "__main__":` block.
-   The `main()` function initializes a single `Library` object, which immediately loads all data from the text files.
-   A `while True:` loop runs continuously, displaying the user menu and capturing input.
-   An `if/elif/else` block routes the user's choice to the corresponding method in the `Library` class, executing the requested operation.
-   The program exits when the user selects the "Exit" option from the menu.
