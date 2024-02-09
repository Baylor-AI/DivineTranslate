import io

# class translation:
#     # what to do on creation of new object; in this case we're passing an empty object back
#     def __new__(cls,*args,**kwargs):
#         return super().__new__()
#
#     # here is the initializer
#     def __init(self, language, version, book, chapter, verse):
#         self.language = language
#         self.version = version
#         self.book = book
#         self.chapter = chapter
#         self.verse = verse
#
#     # here is the toString function
#     def __repr__(self) -> str:
#         return f"{type(self).__name__}(language={self.language}, book={self.book}, chapter={self.chapter}, verse={self.verse}"
#
#     pass

def get_mapping(filename):
    map=[]
        #   TODO: map each line of a translation file to their respective book, chapter, and verse

def to_sql(fileName):
    # TODO: Work on this backend in a different file, later
    file=io.open(fileName, mode="r", encoding="utf-8")
    for line in file:
        file.readline()
        # TODO: send this line to the database

def from_sql(book, chapter, verse, language):
    # TODO: grab the selected verse from the database
    sql=[]


def tokenize(book, chapter, verse, language1, language2):
        # TODO: grab the verse from the database as a token and output it in the form {"language1":"string", "language2","string_translation"}
    token = {
        language1: from_sql(book, chapter,verse,language1),
        language2: from_sql(book, chapter,verse, language2)
    }

    filej=io.open("TokenFile", mode="rw", encoding="utf-8")
        ##TODO: write token to file