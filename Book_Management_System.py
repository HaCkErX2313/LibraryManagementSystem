class Book:
    def __init__(self, title, author, isbn, is_borrowed=False):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_borrowed = is_borrowed

    def borrow(self):
        if not self._is_borrowed:
            self._is_borrowed = True
            return True
        return False

    def return_book(self):
        if self._is_borrowed:
            self._is_borrowed = False
            return True
        return False

    def to_string(self):
        return f"{self._title}|{self._author}|{self._isbn}|{self._is_borrowed}"

    @staticmethod
    def from_string(data):
        title, author, isbn, is_borrowed = data.strip().split("|")
        return Book(title, author, isbn, is_borrowed == 'True')

    def __str__(self):
        status = "Borrowed" if self._is_borrowed else "Available"
        return f"Title: {self._title}, Author: {self._author}, ISBN: {self._isbn}, Status: {status}"

    @property
    def isbn(self):
        return self._isbn

    @property
    def is_borrowed(self):
        return self._is_borrowed


class User:
    def __init__(self, name, user_id, borrowed_books_isbns=None):
        self._name = name
        self._user_id = user_id
        self._borrowed_books_isbns = borrowed_books_isbns or []

    def add_borrowed_book_isbn(self, isbn):
        if isbn not in self._borrowed_books_isbns:
            self._borrowed_books_isbns.append(isbn)

    def remove_borrowed_book_isbn(self, isbn):
        if isbn in self._borrowed_books_isbns:
            self._borrowed_books_isbns.remove(isbn)

    def to_string(self):
        books = ",".join(self._borrowed_books_isbns)
        return f"{self._name}|{self._user_id}|{books}"

    @staticmethod
    def from_string(data):
        parts = data.strip().split("|")
        name = parts[0]
        user_id = parts[1]
        borrowed = parts[2].split(",") if len(parts) > 2 and parts[2] else []
        return User(name, user_id, borrowed)

    def __str__(self):
        return f"User: {self._name} (ID: {self._user_id}), Borrowed Books: {len(self._borrowed_books_isbns)}"

    @property
    def user_id(self):
        return self._user_id

    @property
    def borrowed_books_isbns(self):
        return self._borrowed_books_isbns


class Library:
    def __init__(self):
        self._books = {}  # isbn: Book
        self._users = {}  # user_id: User
        self.load_data()

    def load_data(self):
        try:
            with open("books.txt", "r") as f:
                for line in f:
                    book = Book.from_string(line)
                    self._books[book.isbn] = book
        except:
            pass

        try:
            with open("users.txt", "r") as f:
                for line in f:
                    user = User.from_string(line)
                    self._users[user.user_id] = user
        except:
            pass

    def save_data(self):
        with open("books.txt", "w") as f:
            for book in self._books.values():
                f.write(book.to_string() + "\n")
        with open("users.txt", "w") as f:
            for user in self._users.values():
                f.write(user.to_string() + "\n")

    def add_book(self, book):
        if book.isbn in self._books:
            return False
        self._books[book.isbn] = book
        self.save_data()
        return True

    def remove_book(self, isbn):
        if isbn in self._books and not self._books[isbn].is_borrowed:
            del self._books[isbn]
            self.save_data()
            return True
        return False

    def register_user(self, user):
        if user.user_id in self._users:
            return False
        self._users[user.user_id] = user
        self.save_data()
        return True

    def remove_user(self, user_id):
        if user_id in self._users and not self._users[user_id].borrowed_books_isbns:
            del self._users[user_id]
            self.save_data()
            return True
        return False

    def borrow_book(self, isbn, user_id):
        if isbn in self._books and user_id in self._users:
            book = self._books[isbn]
            user = self._users[user_id]
            if not book.is_borrowed:
                book.borrow()
                user.add_borrowed_book_isbn(isbn)
                self.save_data()
                return True
        return False

    def return_book(self, isbn, user_id):
        if isbn in self._books and user_id in self._users:
            book = self._books[isbn]
            user = self._users[user_id]
            if isbn in user.borrowed_books_isbns:
                book.return_book()
                user.remove_borrowed_book_isbn(isbn)
                self.save_data()
                return True
        return False

    def search_book(self, query):
        query = query.lower()
        return [book for book in self._books.values()
                if query in book._title.lower() or
                   query in book._author.lower() or
                   query in book._isbn]

    def display_all_books(self):
        for book in self._books.values():
            print(book)

    def display_all_users(self):
        for user in self._users.values():
            print(user)

    def display_user_borrowed_books(self, user_id):
        user = self._users.get(user_id)
        if not user:
            print("User not found.")
            return
        for isbn in user.borrowed_books_isbns:
            book = self._books.get(isbn)
            if book:
                print(book)


def main():
    lib = Library()
    while True:
        print("\n--- LIBRARY MENU ---")
        print("1. Add Book")
        print("2. Register User")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Book")
        print("6. Show All Books")
        print("7. Show All Users")
        print("8. Show User's Borrowed Books")
        print("9. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            if lib.add_book(Book(title, author, isbn)):
                print("Book added successfully.")
            else:
                print("Book with this ISBN already exists.")
        elif choice == 2:
            name = input("Enter user name: ")
            user_id = input("Enter user ID: ")
            if lib.register_user(User(name, user_id)):
                print("User registered successfully.")
            else:
                print("User ID already exists.")
        elif choice == 3:
            user_id = input("Enter user ID: ")
            isbn = input("Enter book ISBN: ")
            if lib.borrow_book(isbn, user_id):
                print("Book borrowed successfully.")
            else:
                print("Unable to borrow book.")
        elif choice == 4:
            user_id = input("Enter user ID: ")
            isbn = input("Enter book ISBN: ")
            if lib.return_book(isbn, user_id):
                print("Book returned successfully.")
            else:
                print("Unable to return book.")
        elif choice == 5:
            query = input("Enter title, author, or ISBN to search: ")
            results = lib.search_book(query)
            if results:
                for book in results:
                    print(book)
            else:
                print("No matching books found.")
        elif choice == 6:
            lib.display_all_books()
        elif choice == 7:
            lib.display_all_users()
        elif choice == 8:
            user_id = input("Enter user ID: ")
            lib.display_user_borrowed_books(user_id)
        elif choice == 9:
            print("Thank you for using the library system.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
