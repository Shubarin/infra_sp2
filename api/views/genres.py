from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from ..models.genres import Genre
from ..serializers.genres import GenreSerializer
from ..permissions import IsAdminOrReadOnly
from .categories import MixinViewSet


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
