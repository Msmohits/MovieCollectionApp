from rest_framework import serializers
from .models import Movie, Collection


class SimpleMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class SimpleMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description']


class CollectionSerializer(serializers.ModelSerializer):
    movies = SimpleMovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    movies = SimpleMovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = "__all__"

    def add_movies_to_collection(self, collection, movies_data):
        for movie_data in movies_data:
            movie_id = movie_data.get("movie_id")
            if not movie_id:
                continue
            try:
                movie = Movie.objects.get(movie_id=movie_id)
            except Movie.DoesNotExist:
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

    # def update(self, validated_data):
    #     movies_data = validated_data.pop('movies')
    #     collection = Collection.objects.create(**validated_data)
    #     for movie_data in movies_data:
    #         movie_id = movie_data.get('movie_id')
    #         if not movie_id:
    #             continue
    #         try:
    #             movie = Movie.objects.get(movie_id=movie_id)
    #         except Movie.DoesNotExist:
    #             movie = Movie.objects.create(**movie_data)
    #         collection.movies.add(movie)
    #     return collection
    #     # for movie_data in movies_data:
    #     #     movie, created = Movie.objects.get_or_create(**movie_data)
    #     #     collection.movies.add(movie)
    #     # return collection


class MovieSerializer(serializers.ModelSerializer):
    collections = CollectionSerializer(
        source="collection_set", many=True, read_only=True
    )

    class Meta:
        model = Movie
        fields = "__all__"
