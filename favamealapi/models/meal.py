from django.db import models


class Meal(models.Model):

    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)

    # TODO: Add an user_rating custom properties

    # TODO: Add an avg_rating custom properties
