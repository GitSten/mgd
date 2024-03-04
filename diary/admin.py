from django.contrib import admin
from .models import DiaryEntry, Trigger


class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'get_intensity')
    search_fields = ('user__username', 'date', 'symptoms')
    list_filter = ('date', 'intensity')

    def get_intensity(self, obj):
        return obj.intensity

    get_intensity.admin_order_field = 'intensity'  # Allows column order sorting
    get_intensity.short_description = 'Intensity'  # Renames column head

    # This will prevent ManyToManyField from being listed directly since it's not supported
    # Instead, you could create a method to display a summary of triggers


admin.site.register(DiaryEntry, DiaryEntryAdmin)


# Register the Trigger model

class TriggerAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_tag',)
    readonly_fields = ('icon_tag',)


# Register your models here.
admin.site.register(Trigger, TriggerAdmin)
