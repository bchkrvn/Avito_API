from rest_framework import serializers

from ads.models import Ad, User, Category


class AdSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)
    image = serializers.CharField(read_only=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Ad
        fields = "__all__"
