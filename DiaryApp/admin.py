from django.contrib import admin
from .models import DiaryEntry

@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'mood', 'created_at', 'updated_at')
    list_filter = ('mood', 'created_at')
    search_fields = ('title', 'content')
