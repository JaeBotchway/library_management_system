from django.urls import path
from library.views import (CreateCatalogue, ListCatalogue, DeleteCatalogue, CreateBook, ListBook, 
DetailCatalogue, DetailBook, CreateBookRequest,
UpdateApprovalStatus, UpdateBookAvailabilty, GetBookByAuthor, CreateAuthor, ListAuthor,)



urlpatterns = [
  path('create_catalogue/', CreateCatalogue.as_view(), name='CreateCatalogue'),
  path('list_catalogue/', ListCatalogue.as_view(), name='ListCatalogue'),
  path('detail_catalogue/<int:id>/', DetailCatalogue.as_view(), name='DetailCatalogue'),
  path('delete_catalogue/<int:id>/', DeleteCatalogue.as_view(), name='DeleteCatalogue'),
  path('create_book/', CreateBook.as_view(), name='CreateBook'),
  path('list_book/', ListBook.as_view(), name='ListBook'),
  path('detail_book/<int:id>/', DetailBook.as_view(), name='DetailBook'),
  path('create_bookrequest/', CreateBookRequest.as_view(), name='CreateBookRequest'),
  path('update_approval/<int:id>/', UpdateApprovalStatus.as_view(), name='UpdateApprovalStatus'),
  path('update_date_returned/<int:id>/', UpdateBookAvailabilty.as_view(), name='UpdateBookAvailabilty'),
  path('detail_author/<str:author>/', GetBookByAuthor.as_view(), name='GetBookByAuthor'),
  path('create_author/', CreateAuthor.as_view(), name='CreateAuthor'),
  path('list_author/', ListAuthor.as_view(), name='ListAuthor'),
]