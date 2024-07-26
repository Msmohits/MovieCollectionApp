from rest_framework import serializers
from .models import Movie, Collection


class SimpleCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "description"]


class SimpleMovieSerializer(serializers.ModelSerializer):
    collections = SimpleCollectionSerializer(
        source="collection_set", many=True, read_only=True
    )

    class Meta:
        model = Movie
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = "__all__"

    def add_movies_to_collection(self, collection, movies_data):
        for movie_data in movies_data:
            movie_id = movie_data.get("id")
            if movie_id:
                movie = Movie.objects.get(movie_id=movie_id)
            else:
                movie = Movie.objects.create(**movie_data)
            collection.movies.add(movie)
        return collection

    def create(self, validated_data):
        movies_data = validated_data.pop("movies")
        collection = Collection.objects.create(**validated_data)
        return self.add_movies_to_collection(collection, movies_data)

    def update(self, instance, validated_data):
        movies_data = validated_data.pop("movies")
        instance.movies.clear()
        instance = super().update(instance, validated_data)
        return self.add_movies_to_collection(instance, movies_data)
