from django.contrib import admin
from .models import DiaryEntry


class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date', 'intensity', 'triggers', 'symptoms', 'notes']
    search_fields = ['user__username', 'date', 'triggers', 'symptoms']
    list_filter = ['date', 'intensity']


admin.site.register(DiaryEntry, DiaryEntryAdmin)
