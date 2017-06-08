from django.db import models
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
# Create your models here.

class Book(models.Model):

	title = models.CharField(max_length=256)
	isbn = models.IntegerField(null=True)
	author = models.CharField(max_length=256)
	author_id = models.IntegerField(null=True)
	small_image_url = models.URLField(max_length=200, null=True, blank=True)
	publisher = models.CharField(max_length=256, null=True)
	num_pages = models.IntegerField(null=True)
	series_title = models.CharField(max_length=256, null=True)
	series_id = models.IntegerField(null=True, blank=True, default=0)
	pubyear = models.IntegerField(null=True, blank=True)
	pubday = models.IntegerField(null=True, blank=True)
	pubmonth = models.IntegerField(choices=MONTHS, null=True, blank=True)
	rating = models.CharField(max_length=256, null=True)
	url = models.URLField(max_length=200, null=True, blank=True)
	description = models.CharField(max_length=10000, null=True)

	@property
	def date(self):
		return "{} {}, {}".format(self.get_pubmonth_display(), self.pubday, self.pubyear)
	@property
	def series(self):
		if self.series_title == None:
			return "None"
		else:
			return "<a href='http://www.goodreads.com/series/{}' target='_blank'>{}</a>".format(self.series_id, self.series_title)
class Loans(models.Model):

	date_created = models.DateTimeField(auto_now_add=True)
	borrowed_from = models.CharField(max_length=256)
	borrower = models.CharField(max_length=256, null=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)