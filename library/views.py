from logging import exception
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from accounts.models import UserProfile
from library.models import Catalogue, Book, BookRequest, Author, BookComment
from library.serializers import (BookSerializer, CatalogueSerializer, BookRequestSerializer, 
UpdateApprovalSerializer, UpdateAvailabilitySerializer, BookAuthorSerializer, AuthorSerializer,
BookCommentSerializer)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from library.permission import IsStaffUser
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class CreateCatalogue(generics.CreateAPIView):
    queryset = Catalogue.objects
    serializer_class = CatalogueSerializer
    permission_classes = [IsStaffUser]
    authentication_classes = [JWTAuthentication]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListCatalogue(generics.ListAPIView):
    queryset = Catalogue.objects
    serializer_class = CatalogueSerializer

    def get(self, request):
        serializer = CatalogueSerializer(self.queryset.all(), many=True, context={'request': request})

        return Response({
            'status': 'success',
            'detail': 'Catalogue Successfully listed',
            'data': serializer.data
        })


class DetailCatalogue(generics.ListAPIView):
    queryset = Catalogue.objects
    serializer_class = CatalogueSerializer

    def get(self,request, *args, **kwargs):
        catalogue_id = self.kwargs.get('id')
        catalogue = Catalogue.objects.get(id=catalogue_id)
        obj = Book.objects.filter(catalogue_id=catalogue.id)
        return Response({
            'detail': 'Succesful',
            'data': obj.values()
        })


class DeleteCatalogue(generics.DestroyAPIView):
    queryset = Catalogue.objects
    serializer_class = CatalogueSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser]
    lookup_field = 'id'

    def get_queryset(self):
        catalogue_id = self.kwargs.get('id')
        obj = self.queryset.filter(id=catalogue_id)
        return obj

    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"status": "success",
                         "detail": "Deleted successfully"})


class CreateBook(generics.CreateAPIView):
    queryset = Book.objects
    serializer_class = BookSerializer
    permission_classes = [IsStaffUser]
    authentication_classes = [JWTAuthentication]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListBook(generics.ListAPIView):
    queryset = Book.objects
    serializer_class = BookSerializer

    def get(self, request):
        serializer = BookSerializer(self.queryset.all(), many=True, context={'request': request})

        return Response({
            'status': 'success',
            'detail': 'Book Successfully listed',
            'data': serializer.data
        })

class DetailBook(generics.ListAPIView):
    queryset = Book.objects
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    look_up = 'id'

    def get_queryset(self):
        book_id = self.kwargs.get('id')
        obj = self.queryset.filter(id=book_id)
        return obj


class CreateBookRequest(generics.CreateAPIView):
    queryset = BookRequest.objects
    serializer_class = BookRequestSerializer
    authentication_classes = [JWTAuthentication]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if self.request.user.is_staff:
             return Response({
                'detail': 'Not Authorized'
             })
        book_available = Book.objects.filter(id=request.data.get('book')).first()
        
        if book_available and  book_available.quantity != 0:
            # if book_available and book_available.is_available:
            #     print(book_available, 11, book_available.quantity)
            
            serializer.is_valid(raise_exception=True)
            
            book_available.quantity -= 1
            book_available.save()
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        if book_available and book_available.quantity == 0:
            book_available.is_available = False
            book_available.save()
            return Response({
                'error': 'Book is not available'
            })

class UpdateApprovalStatus(generics.UpdateAPIView):

    queryset = BookRequest.objects
    serializer_class = UpdateApprovalSerializer
    permission_classes = [IsStaffUser]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'


class UpdateBookAvailabilty(generics.UpdateAPIView):
    queryset = BookRequest.objects
    serializer_class = UpdateAvailabilitySerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'


    def update(self, request, *args, **kwargs):
        
        super().update(request, *args, **kwargs)
        return Response({"status": "success",
                        "detail": "Updated successfully"})



class GetBookByAuthor(generics.ListAPIView):
    queryset = Book.objects
    serializer_class = BookAuthorSerializer

    def get(self,request, *args, **kwargs):
        
        author_name = self.kwargs.get('author')
        author = Book.objects.filter(author=author_name).values()
        return Response({
            'detail': 'Succesful',
            'data': author
        })
    

class CreateAuthor(generics.CreateAPIView):
    queryset = Author.objects
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffUser]
    authentication_classes = [JWTAuthentication]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListAuthor(generics.ListAPIView):
    queryset = Author.objects
    serializer_class = AuthorSerializer

    def get(self, request):
        serializer = AuthorSerializer(self.queryset.all(), many=True, context={'request': request})
        return Response({
            'status': 'success',
            'detail': 'Author Successfully listed',
            'data': serializer.data
        })



class CreateComment(generics.CreateAPIView):
    queryset = BookComment.objects
    serializer_class = BookCommentSerializer
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        book = Book.objects.get(id = book_id)
        user_id = UserProfile.objects.get(user=self.request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save(book_id=book.id, user_id=user_id.id)
            return Response({
                    'status': 'success',
                    'detail': 'Comment successfully created',
                    "data": serializer.data
                })
        else:
             return Response('could not comment')



class ListComment(generics.ListAPIView):
    serializer_class = BookCommentSerializer
    lookup_field = 'id'
    def get(self, request):
        serializer = BookCommentSerializer(self.queryset.all(), many=True, context={'request': request})

        return Response({
            'status': 'success',
            'detail': 'Comment Successfully listed',
            'data': serializer.data
        })