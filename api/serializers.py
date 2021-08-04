from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from api.models import Title, Review, Comment, Category, Genre

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'description', 'category', 'genre',
                  'rating']


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    genre = serializers.ListField(write_only=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'description', 'category', 'genre']

    def create(self, validated_data):
        title = Title.objects.create(
            name=validated_data['name'],
            year=validated_data['year'],
            description=validated_data['description'],
            category=Category.objects.get(slug=validated_data['category']))
        try:
            genres_list = validated_data['genre'].split(', ')
        except AttributeError:
            genres_list = validated_data['genre']
        genres = Genre.objects.filter(slug__in=genres_list)
        for genre in genres:
            title.genre.add(genre)
        title.save()
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.year = validated_data.get('year', instance.year)
        if 'category' in validated_data:
            instance.category = Category.objects.get(
                slug=validated_data['category'])
        if 'genre' in validated_data:
            instance.genre.set(Genre.objects.filter(
                slug__in=validated_data['genre']))
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = ['id', 'score', 'text']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'role', 'first_name', 'last_name', 'bio']
