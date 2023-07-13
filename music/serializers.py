from rest_framework import serializers
from .models import Playlist, Track, Genre, FavoriteTrack
from user.serializers import MusicianProfileSerializer
from django.shortcuts import get_object_or_404


class GenreSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Genre
        fields = '__all__'
        read_only = ['name', 'image']


class PlaylistSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Playlist
        exclude = []
        read_only_fields = ('track_count', 'duration_time', 'created_date')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.username
        return data


class TrackSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    mood = serializers.CharField(required=False, allow_null=True, source='mood.name')
    album = serializers.CharField(required=False, allow_null=True, source='album.name')
    genre = serializers.CharField(required=False, allow_null=True, source='genre.name')
    musician = MusicianProfileSerializer()

    class Meta:
        model = Track
        exclude = []
        read_only_fields = ('track', 'duration', 'created_date', 'album', 'genre', 'mood', 'musician')


class FavoriteTrackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    track = TrackSerializer(read_only=True)
    track_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FavoriteTrack
        exclude = []
        read_only_fields = ('like_date',)

    def create(self, validated_data):
        track_id = validated_data['track_id']
        user = validated_data['user']
        track = get_object_or_404(Track, id=track_id)
        favorite_track = FavoriteTrack.objects.get_or_create(user=user, track=track)
        return favorite_track
