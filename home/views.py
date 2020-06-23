from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
import re
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import  LoginForm, UserRegistrationForm
# CommentForm


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm()
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Account Disabled')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def get_category_count():
    queryset = Post.objects.values('category__name').annotate(Count('category__name'))
    return queryset

def index(request):
    posts = Post.objects.order_by('timestamp')[:2]
    featured_posts = Post.objects.filter(featured=True)
    cat_count = get_category_count()
    print (cat_count)
    return render(request, 'index.html', {'posts': posts,'featured_posts': featured_posts, 'cat_count':cat_count})

def programming(request):
    prog_posts = Post.objects.filter(category__name__startswith='programming')
    return render(request, 'programming.html', {'prog_posts': prog_posts})

def gardening(request):
    garden_posts = Post.objects.filter(category__name__startswith='gardening')
    return render(request, 'gardening.html', {'garden_posts': garden_posts})


def about(request):
    return render(request, 'about.html')

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'index:detail.html', {'post':post})

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
    post = Post.objects.filter(id=id)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

