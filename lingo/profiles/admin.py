from django.contrib import admin
from .models import Profile, ProfileLanguage


@admin.register(ProfileLanguage)
class ProfileLanguageAdmin(admin.ModelAdmin):
    list_display = ['profile', 'language', 'tutor']


class ProfileLanguageInline(admin.TabularInline):
    model = ProfileLanguage
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'profile_language', 'timezone']
    inlines = [ProfileLanguageInline]
