from django import forms
from libraryproject.models import Book


class BookForm(forms.Form):
	class Meta:
		model = Book
		fileds = '__all__'


class LoansForm(models.Model):

	loanID = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
	date_created = models.DateField(auto_now_add=True)
	borrowed_from = models.CharField(max_length=256)
	book = models.ForeignKey('Book', on_delete=models.CASCADE)