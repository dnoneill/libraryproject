"""libraryproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from libraryapp import views as views
from libraryapp.views import LoansList, BookList, LoansDetail, BookDetail, AuthorList, AuthorDetail, UserDetail

from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^choose', views.choose, name='choose'),
    url(r'^$', views.home, name='home'),
    url(r'^add', views.add, name='add'),
    url(r'^books/$', BookList.as_view(), name='book_list'),
    url(r'^loans/$', LoansList.as_view(), name='loans_list'),
    url(r'^author/$', AuthorList.as_view(), name='author_list'),
    url(r'^user/(?P<pk>\d+)$', UserDetail.as_view(), name='user_detail'),
    url(r'^author/(?P<pk>\d+)$', AuthorDetail.as_view(), name='author_detail'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='book_detail'),
    url(r'^loans/(?P<pk>\d+)$', LoansDetail.as_view(), name='loans_detail'),
    url(r'^', include('django.contrib.auth.urls')),
]
