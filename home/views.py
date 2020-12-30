from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
import re
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .models import Post, Preference
from .forms import RegisterForm, CommentForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def get_category_count():
    queryset = Post.objects.values('category__name').annotate(Count('category__name'))
    return queryset

def index(request):
    posts = Post.objects.all()[:2]
    featured_posts = Post.objects.filter(featured=True)
    most_recent = Post.objects.order_by('timestamp')[:2]
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

@login_required

def post_detail(request, id):
    post = Post.objects.get(id=id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
    else:
        form = CommentForm()
    return render (request, 'detail.html', {'post': post, 'id': id})

def post_preference(request, id, userprefernce):

    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)

        obj = ''
        valueobj = ''
        try:
            obj= Preference.objects.get(user= request.user, post= post)
            valueobj= obj.value
            valueobj = int(valueobj)
            userpreference = int(userpreference)
            
            if valueobj != userpreference:
                obj.delete()
                
                upref = Preference()
                upref.user = request.user
                upref.post = post
                upref.value = userpreference
                
                if userpreference == 1 and value.obj != 1:
                    post.likes += 1
                    post.dislikes =-1
                    
                elif userpreference == 0 and value.obj != 0:
                    post.dislikes += 1
                    post.likes -= 1
                upref.save()
                post.save()

            elif valueobj == userpreference:
                obj.delete()

                if userpreference == 1:
                    post.likes -= 1
                elif userpreference == 0:
                    post.dislikes -= 1

                post.save()
                return render(request, 'detail.html', {'post':post, 'id': id})
        
        except Preference.DoesNotExist:
            upref = Preference()

            upref.user = request.user
            upref.post = post
            upref.value = userpreference
            user = int(userpreference)
            if userpreference == 1:
                post.likes += 1
            elif userpreference == 2:
                post.dislikes +=1

            upref.save()
            post.save()
            return render (request, 'detail.html', {'post': post, 'id': id})
    else:
        post= get_object_or_404(Post, id=postid)
        return render (request, 'detail.html', {'post': post, 'id': id})



# class  PostDetail(DetailView):
#     model = Post

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)

#         likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
#         liked = False
#         if likes_connected.likes.filter(idd=self.request.user.id).exists():
#             liked = True
#         data['number_of_likes'] = likes_connected.number_of_likes()
#         data['post_is_liked'] = liked
#         return data

    

