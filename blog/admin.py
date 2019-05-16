from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'created_date','status')
    search_fields = ('title', 'content',)
    list_filter = ('status',)
    list_editable = ('status',)
    prepopulated_fields =   {'slug':('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)