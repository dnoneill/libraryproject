from django.shortcuts import render
from django.http import HttpResponse
import xmltodict, json

# Create your views here.
import requests

def choose(request):
	query = request.GET.get('q')
	data = requests.get("https://www.goodreads.com/search/index.xml?key=lTxFf0cwiHnsUItGsSIX9g&q=%s"%query)
	o = xmltodict.parse(data.text)
	books = []
	for work in o['GoodreadsResponse']['search']['results']['work']:
		title = work['best_book']['title']
		author = work['best_book']['author']['name']
		image = work['best_book']['small_image_url']
		try:
			month = work['original_publication_month']['#text']
		except:
			month = work['original_publication_month']['@nil']
		try:
			year = work['original_publication_year']['#text']
		except:
			year = work['original_publication_year']['@nil']
		try:
			day = work['original_publication_day']['#text']
		except:
			day = work['original_publication_day']['@nil']
		date = "%s/%s/%s" % (month, day, year)
		id = work['best_book']['id']['#text']
		rating = work['average_rating']
		url = 'https://www.goodreads.com/book/show/%s' % id
		books.append({'title':title, 'author':author,'image':image, 'date':date,
		'url':url, 'rating':rating, 'id':id})
	return render(request, 'choose.html', {'choices':books})
def post(self, request, *args, **kwargs):
    form = self.get_form()
    if form.is_valid():
        return self.form_valid(form)
    else:
        return self.form_invalid(form)

def form_valid(self, form):
        book = Book()
        book.title = form.cleaned_data['title']
        book.author = form.cleaned_data['author']
        book.save()
        return form_valid(form)
def add(request):
	id = request.GET.get('id')
	info = requests.get("https://www.goodreads.com/book/show.xml?id=%s&key=lTxFf0cwiHnsUItGsSIX9g"%id)
	data = xmltodict.parse(info.text)
	info = {}
	info['title'] = data['GoodreadsResponse']['book']['title']
	info['author'] = data['GoodreadsResponse']['book']['authors']['author']['name']
	info['isbn'] = data['GoodreadsResponse']['book']['isbn']
	info['small_image_url'] = data['GoodreadsResponse']['book']['small_image_url']
	info['publisher'] = data['GoodreadsResponse']['book']['publisher']
	info['num_pages'] = data['GoodreadsResponse']['book']['num_pages']
	info['url'] = data['GoodreadsResponse']['book']['url']
	info['series_works'] = data['GoodreadsResponse']['book']['series_works']
	info['year'] = data['GoodreadsResponse']['book']['publication_year']
	info['day'] = data['GoodreadsResponse']['book']['publication_day']
	info['month'] = data['GoodreadsResponse']['book']['publication_month']
	info['description'] = data['GoodreadsResponse']['book']['description']
	print(data['GoodreadsResponse']['book'].keys())
	
	return render(request, 'form.html', {'info':info})
	
	['id', 'title', 'isbn', 'isbn13', 'asin', 'kindle_asin', 'marketplace_id', 
	'country_code', 'image_url', 'small_image_url', 'publication_year', 
	'publication_month', 'publication_day', 'publisher', 'language_code', 
	'is_ebook', 'description', 'work', 'average_rating', 'num_pages', 'format', 
	'edition_information', 'ratings_count', 'text_reviews_count', 'url', 'link', 
	'authors', 'reviews_widget', 
	'popular_shelves', 'book_links', 'buy_links', 'series_works', 'similar_books']