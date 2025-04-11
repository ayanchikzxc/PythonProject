from django.contrib import admin
from .models import DiaryEntry

admin.site.register(DiaryEntry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
