from django.db import models
<<<<<<< HEAD


=======
import uuid
MONTHS = (
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December")
    )
>>>>>>> f196c7f3091a1bc705f56e742de08d0945e93329
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
	id = models.CharField(primary_key= True, max_length=256)
	month = models.IntegerField(choices=MONTHS, default=0)
	day = models.IntegerField(default=0)
	year = models.IntegerField(default=0)

	@property
	def date(self):
		if self.day == 88:
			return "No Date Avaliable"
		else:
			return "{} {}, {}".format(self.get_Month_display(), self.Day, self.Year)

class Loans(models.Model):

	loanID = models.ForeignKey('Book', to_field='id', related_name='book_id')
	date_created = models.DateField(auto_now_add=True)
	borrowed_from = models.CharField(max_length=256)
	borrower = models.CharField(max_length=256, null=True)
	book = models.ForeignKey('Book', on_delete=models.CASCADE)