from django import forms
from .models import MealEntry, Profile, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {
            "title": "タイトル",
            "content": "本文",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }


class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ["date", "name", "kcal", "protein", "fat", "carb"]
        labels = {
            "date": "日付",
            "name": "食事名",
            "kcal": "カロリー（kcal）",
            "protein": "タンパク質（g）",
            "fat": "脂質（g）",
            "carb": "炭水化物（g）",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "kcal": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "protein": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "fat": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "carb": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["kcal_goal", "protein_goal", "fat_goal", "carb_goal"]
        labels = {
            "kcal_goal": "目標カロリー（kcal）",
            "protein_goal": "目標タンパク質（g）",
            "fat_goal": "目標脂質（g）",
            "carb_goal": "目標炭水化物（g）",
        }
        widgets = {
            "kcal_goal": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "protein_goal": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "fat_goal": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "carb_goal": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }
