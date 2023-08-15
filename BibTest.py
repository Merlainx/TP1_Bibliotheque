import csv
import datetime


class Document:
    def __init__(self, title):
        self.title = title

class Volume(Document):
    def __init__(self, title, author_name):
        super().__init__(title)
        self.author_name = author_name

class Book(Volume):
    def __init__(self, title, author_name):
        super().__init__(title, author_name)
        self.is_available = True

class ComicBook(Volume):
    def __init__(self, title, author_name, illustrator):
        super().__init__(title, author_name)
        self.illustrator = illustrator

class Dictionary(Volume):
    pass

class Newspaper(Document):
    def __init__(self, title, publication_date):
        super().__init__(title)
        self.publication_date = publication_date

class Loan:
    def __init__(self, member, book):
        self.member = member
        self.book = book
        self.borrow_date = datetime.date.today()
        self.return_date = None

class Library:
    def __init__(self):
        self.documents = []
        self.members = []
        self.loans = []

    def add_document(self, document):
        self.documents.append(document)

    def remove_document(self, document):
        self.documents.remove(document)

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    def lend_book(self, member, book):
        if isinstance(book, Book) and book.is_available:
            book.is_available = False
            loan = Loan(member, book)
            self.loans.append(loan)
            member.borrowed_books.append(book)

    def return_book(self, member, book):
        if book in member.borrowed_books:
            book.is_available = True
            member.borrowed_books.remove(book)
            for loan in self.loans:
                if loan.book == book and loan.member == member and loan.return_date is None:
                    loan.return_date = datetime.date.today()

    def save_library(self):
        with open('Biblio.txt', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Author", "Is Available", "Type"])
            for doc in self.documents:
                if isinstance(doc, Book):
                    writer.writerow([doc.title, doc.author_name, doc.is_available, "Book"])
                elif isinstance(doc, ComicBook):
                    writer.writerow([doc.title, doc.author_name, doc.illustrator, "Comic Book"])
                elif isinstance(doc, Newspaper):
                    writer.writerow([doc.title, doc.publication_date, "", "Newspaper"])

    def load_library(self):
        with open('Biblio.txt', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[3] == "Book":
                    self.add_document(Book(row[0], row[1]))
                elif row[3] == "Comic Book":
                    self.add_document(ComicBook(row[0], row[1], row[2]))
                elif row[3] == "Newspaper":
                    self.add_document(Newspaper(row[0], row[1]))

    def save_members(self):
        with open('Adhérents.txt', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["First Name", "Last Name"])
            for member in self.members:
                writer.writerow([member.first_name, member.last_name])

    def load_members(self):
        with open('Adhérents.txt', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                self.add_member(Member(row[0], row[1]))

    def save_loans(self):
        with open('Emprunts.txt', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Member First Name", "Member Last Name", "Book Title", "Borrow Date", "Return Date"])
            for loan in self.loans:
                writer.writerow([loan.member.first_name, loan.member.last_name, loan.book.title, loan.borrow_date, loan.return_date])

    def load_loans(self):
        with open('Emprunts.txt', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                member = next((m for m in self.members if m.first_name == row[0] and m.last_name == row[1]), None)
                book = next((b for b in self.documents if b.title == row[2]), None)
                if member is not None and book is not None:
                    self.lend_book(member, book)
                    self.loans[-1].borrow_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
                    if row[4]:
                        self.loans[-1].return_date = datetime.datetime.strptime(row[4], "%Y-%m-%d").date()

class Member:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.borrowed_books = []

    def borrow_book(self, library, book):
        library.lend_book(self, book)

    def return_book(self, library, book):
        library.return_book(self, book)
