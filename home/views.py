from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
import re
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, LikeDislike

# Create your views here.

def get_category_count():
    queryset = Post.objects.values('category__name').annotate(Count('category__name'))
    return queryset

def index(request):
    posts = Post.objects.order_by('timestamp')[:2]
    featured_posts = Post.objects.filter(featured=True)
    cat_count = get_category_count()
    # print (cat_count)
    return render(request, 'index.html', {'posts': posts,'featured_posts': featured_posts, 'cat_count':cat_count})

def programming(request):
    prog_posts = Post.objects.filter(category__name__startswith='programming')
    return render(request, 'programming.html', {'prog_posts': prog_posts})

def gardening(request):
    garden_posts = Post.objects.filter(category__name__startswith='gardening')
    return render(request, 'gardening.html', {'garden_posts': garden_posts})


def about(request):
    return render(request, 'about.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    return render(request, 'search_results.html', {'queryset': queryset})

def articles(request):
    articles = Post.objects.all()
    return render(request, 'articles.html', {'articles': articles})

def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse("<h3>rozzie</h3>")

def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("rozzie <br> cookie deleted")
    else:
        response = HttpResponse("Rozzie <br> your cookie didn't work!")
    return response


def post_detail(request, id):
    post_detail = Post.objects.get(id=id)
    return render(request, 'post_detail.html', {'post_detail': post_detail})

