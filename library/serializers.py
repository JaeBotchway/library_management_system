from rest_framework import serializers
from library.models import Book, Catalogue, BookRequest, Author, BookComment
from rest_framework.exceptions import APIException

class ResourceNotFound(APIException):
    status_code = 404
    default_detail = {
        "status": "failure",
       "detail": "the given id did not return any data",
    }

class CatalogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogue
        fields = ['id','name', 'description']

        exta_kwargs={
            'description': {'required':False}
        }

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'catalogue', 'timestamp', 'image', 'quantity', 'price', 'discount']

        exta_kwargs={
            'author': {'required':False},
            'image': {'required':False},
            'discount': {'required':False},
            'price': {'required':False},
        }


class BookRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookRequest
        fields = ['user','book', 'date_approved', 'date_returned', 'approval_status']

        exta_kwargs={
            'date_approved': {'required':False},
            'date_returned': {'required':False},
            'approval_status': {'required':False},
            
        }

class UpdateApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRequest
        fields = ['approval_status']
    
    def update(self, instance, validated_data):
            if 'approval_status' in validated_data:
                instance.approval_status = validated_data['approval_status']
            instance.save()
            return instance

class UpdateAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRequest
        fields = ['book', 'date_returned']
    
    def update(self, instance, validated_data):
            if 'date_returned' in validated_data:
                if instance.approval_status == 'approved':
                    instance.date_returned = validated_data['date_returned']
                try: 
                    book =  Book.objects.get(id=instance.book_id) 
                    book.is_available = True 
                    book.quantity += 1
                    book.save()   
                    instance.save()
                    return instance
                except Book.DoesNotExist:
                    raise ResourceNotFound
                


class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['author', 'title', 'catalogue', 'image']

        exta_kwargs={
            'title': {'required':False},
            'catalogue': {'required':False},
            'image': {'required':False},
        }


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id','firstname', 'lastname', 'address', 'country']

        extra_kwargs={
            'address': {'required':False},
            'country': {'required':False},
        }


class BookCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookComment
        fields = ['comment']

        extra_kwargs={

            'user': {'required':False},
            'book': {'required':False},
        }


    