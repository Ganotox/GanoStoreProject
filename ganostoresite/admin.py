from django.contrib import admin
from .models import User, Program, Category, Genre, Comment, Complaint, Rating


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'uploaded_by', 'category', 'genre')
    search_fields = ('title', 'description')
    list_filter = ('category', 'genre', 'uploaded_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('program', 'author', 'content', 'created_at')
    search_fields = ('content', 'author__username', 'program__title')
    list_filter = ('created_at', 'author')


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('program', 'author', 'content', 'created_at', 'resolved')
    search_fields = ('content', 'author__username', 'program__title')
    list_filter = ('resolved', 'created_at')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('program', 'user', 'score')
    search_fields = ('program__title', 'user__username')
    list_filter = ('score',)


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'is_superuser')


# Реєстрація моделей з налаштуваннями
admin.site.register(User, UserAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Rating, RatingAdmin)
