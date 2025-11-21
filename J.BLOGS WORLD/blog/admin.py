from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like, Follow, Profile

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Profile)
