from django.contrib import admin
from .models import Bird
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Bird)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('bird_name', 'bird_count', 'date')
    search_fields = ['bird_name']
    list_filter = ('date',)

    summernote_fields = ('bird_name',)
# Register your models here.
