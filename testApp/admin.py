from django.contrib import admin
from .models import MealEntry, Profile, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "created_at")
    search_fields = ("title", "content", "author__username")
    list_filter = ("created_at",)

@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "name", "kcal", "protein", "fat", "carb", "created_at")
    list_filter = ("date", "user")
    search_fields = ("name",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "kcal_goal", "protein_goal", "fat_goal", "carb_goal")
