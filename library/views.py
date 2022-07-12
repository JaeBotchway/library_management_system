from logging import exception
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from accounts.models import UserProfile
from library.models import Catalogue, Book, BookRequest
from library.serializers import BookSerializer, CatalogueSerializer, BookRequestSerializer, UpdateApprovalSerializer, UpdateAvailabilitySerializer
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
    authentication_classes = [JWTAuthentication]

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
    authentication_classes = [JWTAuthentication]

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
    authentication_classes = [JWTAuthentication]

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
        
        if book_available and book_available.is_available:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            book_available.is_available = False
            book_available.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
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



