"""View module for handling requests about restaurants"""
from crypt import methods
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from favamealapi.models import Restaurant, restaurant
from favamealapi.models.favoriterestaurant import FavoriteRestaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """JSON serializer for restaurants"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'favorite',)


class FaveSerializer(serializers.ModelSerializer):
    """JSON serializer for favorites"""

    class Meta:
        model = FavoriteRestaurant
        exclude = ('restaurant', 'user')


class RestaurantView(ViewSet):
    """ViewSet for handling restuarant requests"""

    def create(self, request):
        """Handle POST operations for restaurants

        Returns:
            Response -- JSON serialized event instance
        """
        rest = Restaurant()
        rest.name = request.data["name"]
        rest.address = request.data["address"]

        try:
            rest.save()
            serializer = RestaurantSerializer(
                rest, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized game instance
        """
        restaurant = Restaurant.objects.get(pk=pk)
        try:
            FavoriteRestaurant.objects.get(
                restaurant=restaurant, user=request.auth.user)

            restaurant.favorite = True

        except FavoriteRestaurant.DoesNotExist:
            restaurant.favorite = False

        serializer = RestaurantSerializer(
            restaurant, context={'request': request})
        
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to restaurants resource

        Returns:
            Response -- JSON serialized list of restaurants
        """
        restaurants = Restaurant.objects.all()
        for restaurant in restaurants:
            try:
                FavoriteRestaurant.objects.get(
                    restaurant_id=restaurant.id, user=request.auth.user)

                restaurant.favorite = True

            except FavoriteRestaurant.DoesNotExist:
                restaurant.favorite = False

        serializer = RestaurantSerializer(
            restaurants, many=True, context={'request': request})
        
        return Response(serializer.data)
    
    @action(methods=['post', 'delete'], detail=True)
    def star(self, request, pk):
        try:
            restuarant_fav = FavoriteRestaurant.objects.get(
                restaurant_id=pk, user_id=request.auth.user_id)
            restuarant_fav.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except FavoriteRestaurant.DoesNotExist:
            serializer = FaveSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.auth.user, restaurant_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
