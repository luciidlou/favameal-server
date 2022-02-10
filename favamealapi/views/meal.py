"""View module for handling requests about meals"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from favamealapi.models import Meal, MealRating, Restaurant, FavoriteMeal
from favamealapi.views.restaurant import RestaurantSerializer


class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals"""
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'restaurant', 'user_rating',
                  'avg_rating', 'is_favorite')
        depth = 1


class CreateMealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals"""
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Meal
        fields = ('name', 'restaurant')


class MealRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealRating
        fields = ('rating',)


class MealFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMeal
        exclude = ('user', 'meal')


class MealView(ViewSet):
    """ViewSet for handling meal requests"""

    def create(self, request):
        """Handle POST operations for meals

        Returns:
            Response -- JSON serialized meal instance
        """
        meal = Meal()
        meal.name = request.data["name"]
        meal.restaurant = Restaurant.objects.get(
            pk=request.data["restaurant"])

        try:
            meal.save()
            serializer = CreateMealSerializer(
                meal, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Handle GET requests for single meal

        Returns:
            Response -- JSON serialized meal instance
        """
        meal = Meal.objects.get(pk=pk)
        try:
            meal_rating = MealRating.objects.get(
                user=request.auth.user, meal=meal)

            meal.user_rating = meal_rating.rating
        except MealRating.DoesNotExist:
            meal.user_rating = 0

        try:
            FavoriteMeal.objects.get(meal=meal, user=request.auth.user)
            meal.is_favorite = True
        except FavoriteMeal.DoesNotExist:
            meal.is_favorite = False

        serializer = MealSerializer(
            meal, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to meals resource

        Returns:
            Response -- JSON serialized list of meals
        """
        meals = Meal.objects.all()

        for meal in meals:
            try:
                meal_rating = MealRating.objects.get(
                    user=request.auth.user, meal=meal)

                meal.user_rating = meal_rating.rating
            except MealRating.DoesNotExist:
                meal.user_rating = 0

            try:
                FavoriteMeal.objects.get(meal=meal, user=request.auth.user)
                meal.is_favorite = True
            except FavoriteMeal.DoesNotExist:
                meal.is_favorite = False

        serializer = MealSerializer(
            meals, many=True, context={'request': request})

        return Response(serializer.data)

    @action(methods=['post', 'put'], detail=True)
    def rate(self, request, pk):

        try:
            user_rating = MealRating.objects.get(
                meal_id=pk, user_id=request.auth.user_id)

            user_rating.rating = request.data['rating']
            user_rating.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except MealRating.DoesNotExist:
            serializer = MealRatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(meal_id=pk, user=request.auth.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post', 'delete'], detail=True)
    def star(self, request, pk):
        try:
            meal_fav = FavoriteMeal.objects.get(
                meal_id=pk, user_id=request.auth.user_id)
            meal_fav.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except FavoriteMeal.DoesNotExist:
            serializer = MealFavoriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.auth.user, meal_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
