import sqlite3
from pandas import DataFrame, Series

class LibraryManagementSystem:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author, genre):
        self.cursor.execute('INSERT INTO books (title, author, genre) VALUES (?, ?, ?)', (title, author, genre))
        self.conn.commit()

    def add_borrower(self, name, phone_number, email):
        self.cursor.execute('INSERT INTO borrowers (name, phone_number, email) VALUES (?, ?, ?)', (name, phone_number, email))
        self.conn.commit()

    def borrow_book(self, book_id, borrower_id):
        self.cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
        book_data = self.cursor.fetchone()
        if book_data:
            self.cursor.execute('SELECT * FROM borrowers WHERE id=?', (borrower_id,))
            borrower_data = self.cursor.fetchone()
            if borrower_data:
                self.cursor.execute('INSERT INTO borrow_history (book_id, borrower_id) VALUES (?, ?)', (book_id, borrower_id))
                self.conn.commit()
                return f'Book {book_data[1]} borrowed by {borrower_data[0]}'
        return 'Error: Book or borrower not found'

    def return_book(self, book_id):
        self.cursor.execute('SELECT * FROM borrow_history WHERE book_id=?', (book_id,))
        borrow_history = self.cursor.fetchall()
        for entry in borrow_history:
            if entry[1] == book_id:
                self.cursor.execute('DELETE FROM borrow_history WHERE book_id=?', (entry[0],))
                self.conn.commit()
                return f'Book {entry[2]} returned'
        return 'Error: Book not found in borrow history'

    def get_all_books(self):
        self.cursor.execute('SELECT * FROM books')
        rows = self.cursor.fetchall()
        df = DataFrame(rows, columns=['id', 'title', 'author', 'genre'])
        return df

    def get_all_borrowers(self):
        self.cursor.execute('SELECT * FROM borrowers')
        rows = self.cursor.fetchall()
        df = DataFrame(rows, columns=['id', 'name', 'phone_number', 'email'])
        return df


def main():
    db_name = 'library.db'
    library_system = LibraryManagementSystem(db_name)
    library_system.create_tables()

    # Add some sample data
    library_system.add_book('To Kill a Mockingbird', 'Harper Lee', 'Fiction')
    library_system.add_book('1984', 'George Orwell', 'Dystopian')
    library_system.add_borrower('John Doe', '1234567890', 'johndoe@example.com')

    # Test some functions
    print(library_system.borrow_book(1, 1))
    print(library_system.return_book(1))
    print(library_system.get_all_books())
    print(library_system.get_all_borrowers())


if __name__ == '__main__':
    main()