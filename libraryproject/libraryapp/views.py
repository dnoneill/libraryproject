from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

import xmltodict, json
from .forms import BookForm, LoansForm
from .models import Book, Loans, Author
# Create your views here.
import requests
def home(request):
    return HttpResponseRedirect("/loans")
    
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
        info['pubyear'] = data['GoodreadsResponse']['book']['publication_year']
        info['pubday'] = data['GoodreadsResponse']['book']['publication_day']
        info['pubmonth'] = data['GoodreadsResponse']['book']['publication_month']
        info['description'] = data['GoodreadsResponse']['book']['description']
        form = LoansForm(initial=info)
        return render(request, 'form.html', {'form':form, 'info':info})
    else:
        form = LoansForm()
        return render(request, 'form.html', {'form':form})
        
class LoansList(FormMixin, ListView):
    model = Loans
    form_class = LoansForm
    ordering = ['-date_created']
    def get_context_data(self, **kwargs):
        context = super(LoansList, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
        
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            author = Author()
            author.author = form.cleaned_data['author']
            author.id = form.cleaned_data['author_id']
            author.save()
            book = Book()
            book.title = form.cleaned_data['title']
            book.author = author
            book.ibsn = form.cleaned_data['isbn']
            book.small_image_url = form.cleaned_data['small_image_url']
            book.publisher = form.cleaned_data['publisher']
            book.num_pages = form.cleaned_data['num_pages']
            book.pubyear = form.cleaned_data['pubyear']
            book.pubday = form.cleaned_data['pubday']
            book.pubmonth = form.cleaned_data['pubmonth']
            book.url = form.cleaned_data['url']
            book.url = form.cleaned_data['url']
            book.description = form.cleaned_data['description']
            book.save()
            loan = Loans()
            loan.borrower = form.cleaned_data['borrower']
            loan.borrowed_from = form.cleaned_data['borrowed_from']
            loan.book = book
            loan.save()
            return HttpResponseRedirect('/loans/')
        else:
            return form.errors

class BookList(ListView):
    model = Book
    ordering = ['-author']

class BookDetail(DetailView):
    model = Book
    
class LoansDetail(DetailView):
    model = Loans
    ordering = ['date_created']

class AuthorDetail(DetailView):
    model = Author
   
    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context

class AuthorList(ListView):
    model = Author
    ordering = ['author']

    