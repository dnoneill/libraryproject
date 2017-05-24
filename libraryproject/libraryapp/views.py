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
		books.append({'title':title, 'author':author,'image':image, 'date':date, 'url':url, 'rating':rating})
	return render(request, 'choose.html', {'choices':books})
	