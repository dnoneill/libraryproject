from django import forms
from .models import Book, Loans, Author
from django.contrib.auth.models import User


class BookForm(forms.Form):
	class Meta:
		model = Book
		fields = '__all__'
class LoansForm(forms.Form):
	choices = User.objects.values_list('id', 'username')
	borrowed_from = forms.ChoiceField(choices=choices)
	borrower = forms.ChoiceField(choices=choices)
	title = forms.CharField(max_length=256)
	isbn = forms.IntegerField(required=False)
	author = forms.CharField(max_length=256, required=False)
	author_id = forms.IntegerField(required=False)
	small_image_url = forms.URLField(max_length=200, required=False)
	publisher = forms.CharField(max_length=256, required=False)
	num_pages = forms.IntegerField(required=False)
	pubyear = forms.IntegerField(required=False)
	pubday = forms.IntegerField(required=False)
	pubmonth = forms.IntegerField(required=False)
	url = forms.URLField(max_length=200, required=False)
	description = forms.CharField(max_length=10000, required=False)
    