# Smart Library Management System

## How to Run the Program

### Prerequisites
- Python 3.x

### Steps
1.  **Open a terminal** or command prompt in the project's root directory.

2.  **(Optional but Recommended) Create and activate a virtual environment:**
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

4.  You will see a menu of options. Enter the number corresponding to the action you want to perform and follow the on-screen prompts.

---

## Implementation Walkthrough

This document provides a detailed explanation of how the Smart Library Management System is implemented.

### 1. Project Structure

The project consists of the following files:

-   `main.py`: The main source file containing all the Python code for the system, including class definitions and the main application logic.
-   `books.txt`: A text file used to persistently store the library's book records.
-   `members.txt`: A text file used to persistently store the library's member records.
-   `transactions.log`: A log file that records every borrow and return transaction with a timestamp.
-   `README.txt`: This file.

### 2. Core Classes

The system is built on Object-Oriented principles and uses three main classes:

#### a. `Book` Class
-   **Purpose:** Represents a single book in the library.
-   **Attributes:**
    -   `book_id`: A unique identifier for the book.
    -   `title`: The title of the book.
    -   `author`: The author of the book.
    -   `available_copies`: The number of copies currently available for borrowing.
-   **Methods:**
    -   `display_info()`: Prints the details of the book in a formatted way.
    -   `update_copies(number)`: Increases or decreases the count of available copies.

#### b. `Member` Class
-   **Purpose:** Represents a single library member.
-   **Attributes:**
    -   `member_id`: A unique identifier for the member.
    -   `name`: The name of the member.
    -   `borrowed_books`: A list of titles of the books the member has currently borrowed.
-   **Methods:**
    -   `borrow_book(book)`: Adds a book title to the member's `borrowed_books` list.
    -   `return_book(book)`: Removes a book title from the `borrowed_books` list.
    -   `display_member_info()`: Prints the member's details and the list of books they have borrowed.

#### c. `Library` Class
-   **Purpose:** Acts as the central controller for the entire system. It manages the collections of books and members and orchestrates all major operations.
-   **Attributes:**
    -   `books`: A list of `Book` objects.
    -   `members`: A list of `Member` objects.
    -   `borrow_count`: A dictionary to track how many times each book has been borrowed.
-   **Key Methods:**
    -   `add_book(book)` / `add_member(member)`: Adds new objects to the library's lists and immediately saves the updated lists to their respective text files.
    -   `borrow_transaction(...)` / `return_transaction(...)`: Handles the logic for borrowing and returning books. This includes finding the member and book, checking for errors (e.g., book unavailable), updating the book's copy count, and updating the member's borrowed list.
    -   `save_books()` / `load_books()`: Handles writing and reading the `books` list to/from `books.txt`. `load_books` is called when the library is initialized to load existing data.
    -   `save_members()` / `load_members()`: Handles writing and reading the `members` list to/from `members.txt`.
    -   `log_transaction(message)`: Writes a timestamped entry to `transactions.log` for every borrow or return action.
    -   `search_by_author(author_name)`: Filters and displays all books by a given author.
    -   `most_borrowed_book()`: Calculates and displays which book(s) have been borrowed the most by reading the `transactions.log`.
    -   `generate_transaction_report()`: Reads and displays the entire contents of `transactions.log`.

### 3. Data Persistence

-   **Book and Member Data:** When a book or member is added, the entire list of books/members is rewritten to `books.txt` or `members.txt`. The data is stored in a comma-separated format. For members, borrowed books are stored as a semicolon-separated list within the same line.
-   **Transaction Logging:** The `transactions.log` file is opened in append mode (`"a"`), so every new transaction is added to the end of the file without overwriting previous logs.

### 4. Main Execution Logic

-   The script is executed starting from the `if __name__ == "__main__":` block.
-   The `main()` function is called, which initializes a single `Library` object. When the `Library` is initialized, it automatically calls `load_books()` and `load_members()` to populate its lists with any data saved from previous sessions.
-   An infinite `while True:` loop starts, which continuously displays the main menu and prompts the user for a choice.
-   An `if/elif/else` block directs the user's choice to the corresponding method in the `Library` class.
-   The loop breaks and the program exits only when the user selects the "Exit" option.