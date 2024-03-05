from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


class Trigger(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='trigger_icons/')  # Specify the directory where icons will be stored

    def __str__(self):
        return self.name

    def icon_tag(self):
        if self.icon:
            return format_html('<img src="{}" style="height:30px;"/>', self.icon.url)
        return "-"
    icon_tag.short_description = 'Icon'
    icon_tag.allow_tags = True


class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    intensity = models.IntegerField()
    other_triggers = models.TextField(blank=True)
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    triggers = models.ManyToManyField(Trigger, blank=True)

    def __str__(self):
        return f"{self.date} - {self.intensity}"
