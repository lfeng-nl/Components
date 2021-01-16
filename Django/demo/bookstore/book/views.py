from django.shortcuts import render
from .models import Author, Book, Comment
from django.http import HttpResponse
from .forms import CommentForm
# Create your views here.

def home(request):
    book_set = Book.objects.all()
    return render(request, 'home.html', {'book_set':book_set})

def book(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
    else:
        form = CommentForm()
    book_id = int(request.GET.get('book_id'))
    if book_id:
        try:
            book = Book.objects.get(id=book_id)
        except :
            pass
        else:
            if book:
                return render(request, 'book.html', {'book':book, 'authors':book.authors.all(), 'commands':book.comments.all(), 'form':form})
    return render(request, 'home.html')

def author(request):
    author_id = request.GET.get('author_id')
    if author_id:
        try:
            author = Author.objects.get(id=author_id)
            books = author.books.all()
        except :
            pass
        else:
            return render(request, 'author.html', {'author':author, 'books':books})
        
    return render(request, 'home.html')