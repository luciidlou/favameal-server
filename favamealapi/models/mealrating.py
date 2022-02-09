from django.contrib.auth.models import User
from django.db import models


class MealRating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mealrating")
    meal = models.ForeignKey(
        "Meal", on_delete=models.CASCADE, related_name="mealrating")
    rating = models.IntegerField()
