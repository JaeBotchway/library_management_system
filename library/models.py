from django.db import models
from accounts.models import UserProfile

# Create your models here.


STATUS = [
    ('approved', 'Approved'),
    ('unapproved', 'Unapproved')
]


class Catalogue(models.Model):
    name = models.CharField(max_length=255)
    description= models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):
    firstname = models.CharField(max_length=255,blank=True, null=True)
    lastname = models.CharField(max_length=255,blank=True, null=True)
    address = models.CharField(max_length=255,blank=True, null=True)
    country = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.firstname

    class Meta:
        ordering = ['lastname']

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images',max_length=255,
        blank=True,
        null=True,)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.title} by {self.author} added to {self.catalogue}" 


class BookRequest(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_approved = models.DateTimeField(auto_now=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    approval_status = models.CharField(choices=STATUS, default='unapproved', max_length=100)

    class Meta:
        ordering = ['date_approved']

    def __str__(self):
        return f"{self.book} was {self.approval_status} "

    @property
    def is_book_returned(self):
        return bool(self.date_returned)