from django.db import models
from favamealapi.models.mealrating import MealRating


class Meal(models.Model):

    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)

    @property
    def user_rating(self):
        return self.__user_rating

    @user_rating.setter
    def user_rating(self, value):
        self.__user_rating = value
        
        
    @property
    def is_favorite(self):
        return self.__is_favorite

    @is_favorite.setter
    def is_favorite(self, value):
        self.__is_favorite = value

    @property
    def avg_rating(self):
        meal_ratings = MealRating.objects.filter(meal_id=self.id)
        total_rating = 0
        if len(meal_ratings) > 0:
            for rating in meal_ratings:
                total_rating += rating.rating
            avg = total_rating / len(meal_ratings)
        else:
            avg = total_rating
        return avg
