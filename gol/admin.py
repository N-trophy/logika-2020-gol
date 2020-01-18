from django.contrib import admin
from gol.models import Task, Post, Parse, TaskCategory


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order')
    ordering = ['order']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name')
    ordering = ['id']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'published', 'text')
    list_filter = ('id', 'author', 'published')
    ordering = ['published']


@admin.register(Parse)
class ParseAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'input_text', 'params', 'datetime',
                    'state', 'report', 'evaluation_time', 'parsed')
    list_filter = ('user', 'task', 'datetime', 'state', 'report')
    ordering = ['-datetime']
