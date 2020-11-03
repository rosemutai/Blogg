from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
import re
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post, LikeDislike
from .forms import  LoginForm, UserRegistrationForm
# CommentForm


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "login.html", {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm()
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Account Disabled')
#             else:
#                 return HttpResponse('Invalid Login')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

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

def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())
# @login_required
# def postpreference(request, postid, userpreference):
#     if request.method == "POST":
#         post = get_object_or_404(Post, id=postid)
#         obj = ""
#         valueobj = ""
#         try:
#             obj = LikeDislike.objects.get(user=request.user, post=post)
#             valueobj = obj.value #value of userpreference
#             valueobj = int(valueobj)
#             userpreference = int(preference)
#             if valueobj != userpreference:
#                 obj.delete()
#                 upref = LikeDislike()
#                 upref.user = request.user

#                 upref.post = post
#                 upref.value = userpreference

#                 if userpreference == 1 and valueobj != 1:
#                     post.likes += 1
#                     post.dislikes -=1
#                 elif userprefence == 2 and valueobj !=2:
#                     post.dislikes += 1
#                     post.likes  -=1
#                 upref.save()
#                 post.save()

#                 return render(request, 'post_detail.html', {'post': post, 'postid':postid})
#             elif valueobj == userprefence:
#                 obj.delete()
#                 if userpreference == 1:
#                     post.likes -=1
#                 elif userpreference == 2:
#                     post.dislikes -= 1
#                 post.save()

#                 return render(request, 'post_detail.html', {'post': post, 'postid': postid})
#         except LikeDislike.DoesNotExist:
#             upref = LikeDislike()
#             upref.user = request.user
#             upref.post = post
#             upref.value = userpreference
#             userpreference = int(userpreference)
#             if  userprefence == 1:
#                 post.likes += 1
#             elif userpreference == 2:
#                 post.dislikes += 1
#             upref.save()
#             post.save()
#             return render(request, 'post_detail.html', {'post': post, 'postid': postid})
#     else:
#         post= get_object_or_404(Post, id=postid)
#         return render(request, 'post_detail.html', {'post': post, 'postid': postid})
