from rest_framework import serializers

from ..models.categories import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category
