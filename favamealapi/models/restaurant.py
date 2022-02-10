from django.db import models


class Restaurant(models.Model):

    name = models.CharField(max_length=55, unique=True)
    address = models.CharField(max_length=255)

    @property
    def favorite(self):
        return self.__favorite

    @favorite.setter
    def favorite(self, value):
        self.__favorite = value
