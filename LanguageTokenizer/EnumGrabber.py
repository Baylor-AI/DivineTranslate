from aenum import Enum, extend_enum

# The enum that stores the mapping between books and their codes
class BooksEnum(Enum):
    none = 0

def AddBook(bookName, bookNumber):
    extend_enum(BooksEnum,bookName, bookNumber)
    print()