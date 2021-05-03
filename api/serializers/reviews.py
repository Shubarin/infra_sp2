from rest_framework import serializers

from ..models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, attrs):
        if not self.context['request'].method == 'POST':
            return attrs
        author = self.context['request'].user
        title = self.context['request'].parser_context['view'].kwargs.get(
            'title_id')
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'You can write only one review to this title.'
            )
        return attrs
