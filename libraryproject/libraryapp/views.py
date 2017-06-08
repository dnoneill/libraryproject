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
    try:
        info['series_title'] = data['GoodreadsResponse']['book']['series_works']['series_work']['series']['title']
        info['series_id'] = data['GoodreadsResponse']['book']['series_works']['series_work']['series']['id']
    except:
        info['series_title'] = data['GoodreadsResponse']['book']['series_works']
    info['year'] = data['GoodreadsResponse']['book']['publication_year']
    print(info['year'])
    info['day'] = data['GoodreadsResponse']['book']['publication_day']
    info['month'] = data['GoodreadsResponse']['book']['publication_month']
    info['description'] = data['GoodreadsResponse']['book']['description']

    return render(request, 'form.html', {'info':info})
    
def lend(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = Book()
            book.title = request.POST['title']
            book.author = request.POST['author']
            book.author_id = request.POST['author_id']
            book.ibsn = request.POST['isbn']
            book.small_image_url = request.POST['image_url']
            book.publisher = request.POST['publisher']
            book.num_pages = request.POST['num_pages']
            book.series_title = request.POST['series_title']
            if request.POST['series_id'] == '':
                book.series_id = 0
            else:
                book.series_id = request.POST['series_id']
            if request.POST['year'] != 'None':
            	book.pubyear = request.POST['year']
            if request.POST['day'] != 'None':
            	book.pubday = request.POST['day']
            if request.POST['month'] != 'None':
            	book.pubmonth = request.POST['month']
            book.url = request.POST['url']
            book.description = request.POST['description']
            book.save()
            loan = Loans()
            loan.borrower = request.POST['lendee']
            loan.borrowed_from = request.POST['lender']
            loan.book = book
            loan.save()
            return HttpResponseRedirect('/books')
    else:
        form = BookForm()

    return HttpResponse("success")

class LoansList(ListView):
    model = Loans
    #form_class = LoanForm
    ordering = ['-date_created']
    
class BookList(ListView):
    model = Book
    #paginate_by = 50
    ordering = ['title']

class BookDetail(DetailView):
    model = Book
    
class LoansDetail(DetailView):
    model = Loans
    