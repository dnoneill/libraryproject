from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User

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
class Author(models.Model):
	author = models.CharField(max_length=2000, null=True)
	
class Book(models.Model):

	title = models.CharField(max_length=256)
	isbn = models.IntegerField(null=True)
	author = models.ForeignKey(Author, related_name='books')
	small_image_url = models.URLField(max_length=200, null=True, blank=True)
	publisher = models.CharField(max_length=256, null=True)
	num_pages = models.IntegerField(null=True)
	pubyear = models.IntegerField(null=True, blank=True, default=0)
	pubday = models.IntegerField(null=True, blank=True)
	pubmonth = models.IntegerField(choices=MONTHS, null=True, blank=True)
	rating = models.CharField(max_length=256, null=True)
	url = models.URLField(max_length=200, null=True, blank=True)
	description = models.CharField(max_length=10000, null=True)

	@property
	def date(self):
		if self.pubmonth != None and self.pubday != None and self.pubyear != None:
			return "{} {}, {}".format(self.get_pubmonth_display(), self.pubday, self.pubyear)
		elif self.pubmonth == None and self.pubday == None and self.pubyear == None:
			return "No Date Avaliable"
		elif self.pubmonth == None and self.pubday == None:
			return "{}".format(self.pubyear)
		elif self.pubmonth != None and self.pubyear != None:
			return "{} {}".format(self.get_pubmonth_display(), self.pubyear)
		elif self.pubday != None and self.pubyear != None:
			return "{}".format(self.pubyear)
			 
class Loans(models.Model):

	date_created = models.DateTimeField(auto_now_add=True)
	borrowed_from = models.ForeignKey(User, related_name='borrowed_from')
	borrower = models.ForeignKey(User, related_name='borrower')
	book = models.ForeignKey(Book, related_name='loans')

	@property
	def timesince(self):
		#print(datetime.datetime.now(timezone.utc))
		if self.date_created != None:
			diff = timezone.now().replace(microsecond=0) - self.date_created.replace(microsecond=0)
			days = diff.days
			hours = diff.seconds // 3600
			min = diff.seconds % 3600 / 60
			if int(min) == 0:
				return "0 minutes"
			if days != 0:
				if hours == 1:
					return "{} days, {} hour".format(days, hours)
				else:
					return "{} days, {} hours".format(days, hours)
			elif days == 0 and hours == 0:
				if int(min) == 1:
					return "{} minute".format(int(min))
				else:
					return "{} minutes".format(int(min))
			elif days == 0:
				if hours == 1 and int(min) == 1:
					return "{} hour {} minute".format(hours, int(min))
				elif int(min) == 1:
					return "{} hours {} minute".format(hours, int(min))
				elif hours == 1:
					return "{} hour {} minutes".format(hours, int(min))
				else:
					return "{} hours {} minutes".format(hours, int(min))
