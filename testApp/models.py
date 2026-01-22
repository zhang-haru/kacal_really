from django.conf import settings
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="no title")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kcal_goal = models.PositiveIntegerField(default=2000)
    protein_goal = models.PositiveIntegerField(default=120)
    fat_goal = models.PositiveIntegerField(default=60)
    carb_goal = models.PositiveIntegerField(default=250)

    def __str__(self):
        return f"profile({self.user.username})"

class MealEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=100)
    kcal = models.PositiveIntegerField()
    protein = models.PositiveIntegerField(default=0)
    fat = models.PositiveIntegerField(default=0)
    carb = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.date} {self.name} ({self.kcal}kcal)"
