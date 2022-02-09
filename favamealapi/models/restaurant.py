from django.db import models


class Restaurant(models.Model):

    name = models.CharField(max_length=55, unique=True)
    address = models.CharField(max_length=255)

    # TODO: Add a `favorite` custom property