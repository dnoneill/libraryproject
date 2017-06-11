from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView

import xmltodict, json
from .forms import BookForm
from .models import Book, Loans
# Create your views here.
import requests
def home(request):
    return render(request, 'home.html')
    
def choose(request):
    query = request.GET.get('q')
    data = requests.get("https://www.goodreads.com/search/index.xml?key=lTxFf0cwiHnsUItGsSIX9g&q=%s"%query)
    o = xmltodict.parse(data.text)
    books = []
    if o['GoodreadsResponse']['search']['total-results'] == '1':
        work = o['GoodreadsResponse']['search']['results']['work']
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
        try:
            rating = work['average_rating']['#text']
        except:
            rating = work['average_rating']
        url = 'https://www.goodreads.com/book/show/%s' % id
        books.append({'title':title, 'author':author,'image':image, 'date':date,
        'url':url, 'rating':rating, 'id':id})
    else:
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
            try:
                rating = work['average_rating']['#text']
            except:
                rating = work['average_rating']
            url = 'https://www.goodreads.com/book/show/%s' % id
            books.append({'title':title, 'author':author,'image':image, 'date':date,
            'url':url, 'rating':rating, 'id':id})
    return render(request, 'choose.html', {'choices':books})
def add(request):
    id = request.GET.get('id')
    if id != None:
        info = requests.get("https://www.goodreads.com/book/show.xml?id=%s&key=lTxFf0cwiHnsUItGsSIX9g"%id)
        data = xmltodict.parse(info.text)
        info = {}
        info['title'] = data['GoodreadsResponse']['book']['title']
        try:
            info['author'] = data['GoodreadsResponse']['book']['authors']['author']['name']
            info['author_id'] = data['GoodreadsResponse']['book']['authors']['author']['id']
        except:
            info['author'] = data['GoodreadsResponse']['book']['authors']['author'][0]['name']
            info['author_id'] = data['GoodreadsResponse']['book']['authors']['author'][0]['id']
        info['isbn'] = data['GoodreadsResponse']['book']['isbn']
        info['small_image_url'] = data['GoodreadsResponse']['book']['small_image_url']
        info['publisher'] = data['GoodreadsResponse']['book']['publisher']
        info['num_pages'] = data['GoodreadsResponse']['book']['num_pages']
        info['url'] = data['GoodreadsResponse']['book']['url']
        info['year'] = data['GoodreadsResponse']['book']['publication_year']
        info['day'] = data['GoodreadsResponse']['book']['publication_day']
        info['month'] = data['GoodreadsResponse']['book']['publication_month']
        info['description'] = data['GoodreadsResponse']['book']['description']

        return render(request, 'form.html', {'info':info})
    else:
        return render(request, 'form.html', {})
    
def lend(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            book = Book()
            if request.POST['title'] != 'None' or request.POST['title'] != '\n':
                book.title = request.POST['title']
            if request.POST['author'] != 'None' or request.POST['author'] != '\n':
                book.author = request.POST['author']
            if request.POST['author_id'] != 'None' or request.POST['author_id'] != '\n':
                book.author_id = request.POST['author_id']
            if request.POST['isbn'] != 'None' or request.POST['isbn'] != '\n':
                book.ibsn = request.POST['isbn']
            if request.POST['image_url'] != 'None' or request.POST['image_url'] != '\n':
                book.small_image_url = request.POST['image_url']
            if request.POST['publisher'] != 'None' or request.POST['publisher'] != '\n':
                book.publisher = request.POST['publisher']
            if request.POST['num_pages'] != 'None' or request.POST['num_pages'] != '\n':
                book.num_pages = request.POST['num_pages']
            if request.POST['num_pages'] == 'None':
            	book.num_pages = 0
            if request.POST['year'] != 'None' or request.POST['year'] != '\n':
                book.pubyear = request.POST['year']
            if request.POST['day'] != 'None' or request.POST['day'] != '\n':
                book.pubday = request.POST['day']
            if request.POST['month'] != 'None' or request.POST['month'] != '\n':
                book.pubmonth = request.POST['month']
            if request.POST['url'] != 'None' or request.POST['url'] != '\n':
                book.url = request.POST['url']
            if request.POST['year'] == 'None':
                book.pubyear = 0
            if request.POST['day'] == 'None':
                book.pubday = 0
            if request.POST['month'] == 'None':
                book.pubmonth = 0
            if request.POST['url'] != 'None' or request.POST['url'] != '\n':
                book.url = request.POST['url']
            if request.POST['description'] != 'None' or request.POST['description'] != '\n':
                book.description = request.POST['description']
            book.save()
            loan = Loans()
            loan.borrower = request.POST['lendee']
            loan.borrowed_from = request.POST['lender']
            loan.book = book
            loan.save()
            return HttpResponseRedirect('/loans/')
    else:
        form = BookForm()

    return HttpResponseRedirect("/loans")

class LoansList(ListView):
    model = Loans
    ordering = ['-date_created']
    
class BookList(ListView):
    model = Book
    ordering = ['title']

class BookDetail(DetailView):
    model = Book
    
class LoansDetail(DetailView):
    model = Loans
    