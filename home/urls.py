from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('category', views.get_category_count, name='category'),
    path('programming', views.programming, name="programming"),
    path('gardening', views.gardening, name="gardening"),
    path('search', views.search, name="search"),
    # path('comment', views.comment, name="comment"),
    path('articles', views.articles, name="articles"),
    path('testcookie', views.cookie_session, name="testcookie"),
    path('deletecookie', views.cookie_delete, name="deletecookie"),
    path('postdetail/<int:id>/', views.post_detail, name='post_detail'),
    # path('postdetail/<int:id>/<userpreference>', views.post_preference, name='post-preference'),
    path('/<userprefernce>/', views.post_preference, name='post-preference'),
    # path('preference/<int:postid>/userprefernce/<int:userpreference>/', views.postpreference, name='postpreference'),
]