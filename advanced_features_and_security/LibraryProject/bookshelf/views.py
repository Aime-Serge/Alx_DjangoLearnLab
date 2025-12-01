from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
from .models import Article
from django.shortcuts import render, get_object_or_404
from .models import Book
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ExampleForm, ArticleForm

def contact_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
        else:
            return render(request, 'bookshelf/form_example.html', {'form': form})
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

def my_view(request):
    response = HttpResponse("Hello, world!")
    response['Content-Security-Policy'] = "default-src 'self';"
    return response

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

@login_required
@permission_required('app_name.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

@login_required
@permission_required('app_name.can_create', raise_exception=True)

def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            response = render(request, 'article_detail.html', {'article': article})
            response['Content-Security-Policy'] = "default-src 'self';"
            return response
    else:
        form = ArticleForm()
    response = render(request, 'article_form.html', {'form': form})
    response['Content-Security-Policy'] = "default-src 'self';"
    return response

@login_required
@permission_required('app_name.can_edit', raise_exception=True)
def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            response = render(request, 'article_detail.html', {'article': article})
            response['Content-Security-Policy'] = "default-src 'self';"
            return response
    else:
        form = ArticleForm(instance=article)
    response = render(request, 'article_form.html', {'form': form, 'article': article})
    response['Content-Security-Policy'] = "default-src 'self';"
    return response

@login_required
@permission_required('app_name.can_delete', raise_exception=True)
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        article.delete()
        return render(request, 'article_list.html')
    return render(request, 'article_confirm_delete.html', {'article': article})