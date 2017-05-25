from django.db import models
import uuid

# Create your models here.

class Book(models.Model):

	title = models.CharField(max_length=256)
	author = models.CharField(max_length=256)
	image = models.URLField(max_length=200, null=True, blank=True)
	date = models.DateField()
	rating = models.CharField(max_length=256)
	url = models.URLField(max_length=200, null=True, blank=True)
	id = models.CharField(primary_key= True, max_length=256)

class Loans(models.Model):

	loanID = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
	date_created = models.DateField(auto_now_add=True)
	borrowed_from = models.CharField(max_length=256)
	book = models.ForeignKey('Book', on_delete=models.CASCADE)