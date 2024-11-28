from django.contrib import admin
from .models import Post

# Rejestracja modelu Post w panelu admina
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')  # Kolumny wyświetlane w tabeli
    search_fields = ('title', 'content')  # Umożliwia wyszukiwanie po tytule i treści
    list_filter = ('created_at',)  # Umożliwia filtrowanie po dacie utworzenia
    ordering = ('-created_at',)  # Porządkowanie po dacie utworzenia (od najnowszych)
