from django.contrib import admin
from library.models import Catalogue, Book, BookRequest

# Register your models here.
admin.site.register(Catalogue)
admin.site.register(Book)
admin.site.register(BookRequest) 