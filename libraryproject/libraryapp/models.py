from django.db import models


# Create your models here.

class Book(models.Model):

	title = models.CharField(max_length=256)
	isbn = models.IntegerField(null=True)
	author = models.CharField(max_length=256)
	small_image_url = models.URLField(max_length=200, null=True, blank=True)
	publisher = models.CharField(max_length=256, null=True)
	num_pages = models.IntegerField(null=True)
	series_works = models.CharField(max_length=256, null=True)
	publication_year = models.CharField(max_length=256, null=True)
	publication_day = models.CharField(max_length=256, null=True)
	publication_month = models.CharField(max_length=256, null=True)
	rating = models.CharField(max_length=256, null=True)
	url = models.URLField(max_length=200, null=True, blank=True)
	id = models.CharField(primary_key= True, max_length=256, default='0')

class Loans(models.Model):

	loanID = models.ForeignKey('Book', to_field='id', related_name='book_id')
	date_created = models.DateField(auto_now_add=True)
	borrowed_from = models.CharField(max_length=256)
	borrower = models.CharField(max_length=256, null=True)
	book = models.ForeignKey('Book', on_delete=models.CASCADE)