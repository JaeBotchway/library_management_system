from django.contrib import admin
from library.models import Catalogue, Book, BookRequest, Author

# Register your models here.
admin.site.register(Catalogue)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookRequest) 