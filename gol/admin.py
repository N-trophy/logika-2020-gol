from django.contrib import admin
from gol.models import Task, Post, Parse, TaskCategory, Submission


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
    list_display = ('id', 'user', 'task', 'input_text', 'params', 'datetime',
                    'state', 'evaluation_time', 'report', 'parsed')
    list_filter = ('user', 'task', 'datetime', 'state', 'report',
                   'evaluation_time')
    ordering = ['-datetime']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'datetime', 'int_status', 'ok',
                    'points', 'user_report', 'int_report')
    list_filter = ('user', 'task', 'ok', 'int_status', 'points',
                   'user_report', 'int_report')
    ordering = ['-datetime']
