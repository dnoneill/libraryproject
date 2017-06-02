from django.db import models
import uuid
MONTHS = (
	(0, "unavaliable"),
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
# Create your models here.

class Book(models.Model):

	title = models.CharField(max_length=256)
	author = models.CharField(max_length=256)
	image = models.URLField(max_length=200, null=True, blank=True)
	date = models.DateField()
	rating = models.CharField(max_length=256)
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

	loanID = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
	date_created = models.DateField(auto_now_add=True)
	borrowed_from = models.CharField(max_length=256)
	book = models.ForeignKey('Book', on_delete=models.CASCADE)