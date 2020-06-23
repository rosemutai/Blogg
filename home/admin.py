from django.contrib import admin
from .models import Category, Post, PostComment

# Register your models here.
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostComment, PostCommentAdmin)


