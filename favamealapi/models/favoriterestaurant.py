from django.contrib.auth.models import User
from django.db import models


class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userfavoriterestaurants")
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="userfavoriterestaurants")
