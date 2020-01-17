from django.contrib import admin
from gol.models.task import Task
from gol.models.post import Post


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'published', 'text')
    list_filter = ('id', 'author', 'published')
    ordering = ['published']
