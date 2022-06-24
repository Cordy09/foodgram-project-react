from django.db import IntegrityError
from django.db.models import Model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Recipe
from .serializers import RecipeInfoSerializer


class RetrieveListViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    pass


class CreateDestroy(viewsets.ModelViewSet):
    serializer_class = RecipeInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'delete']

    def perform_create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            self.queryset.create(
                recipe=recipe, user=request.user
            )
            serializer = RecipeInfoSerializer(
                instance=recipe, context={'request': request}
            )
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            data = {'errors': 'Уже есть'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            self.queryset.get(recipe=recipe, user=request.user).delete()
        except Model.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
