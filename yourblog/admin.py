from django.contrib import admin
from .models import Post, Comment, KeyWords



class PostAdmin(admin.ModelAdmin):
    fields =  ['author', 'title', 'text','created_date','published_date', 'keywords']
    list_display= ('author', 'title','created_date','published_date')
    search_fields = ['title']


class KeywordsAdmin(admin.ModelAdmin):
    fields = ['name']



admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(KeyWords, KeywordsAdmin)
