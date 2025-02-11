from rest_framework import generics, status
from rest_framework.response import Response

from .models import Playlist, Track, TrackInPlaylist, Genre, FavoriteTrack
from .serializers import PlaylistSerializer, TrackSerializer, GenreSerializer, FavoriteTrackSerializer, \
    TrackModifySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsMusician, IsTrackCreator
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class GenreAPIView(generics.ListAPIView):
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Genre.objects.all()


class TrackViewSet(ModelViewSet):
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Track.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsMusician()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTrackCreator()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return TrackModifySerializer
        return TrackSerializer


class FavoriteTrackViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = FavoriteTrackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FavoriteTrack.objects.filter(user=user)


class PlaylistViewSet(ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)

    @action(methods=['post'], detail=True)
    def add_track(self, request, pk=None, track_id=None):
        playlist = self.get_object()

        if track_id:
            track = get_object_or_404(Track, id=track_id)
            existing_track = TrackInPlaylist.objects.filter(playlist=playlist, track=track).exists()

            if existing_track:
                return Response({'detail': 'Track already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            TrackInPlaylist.objects.create(playlist=playlist, track=track)
            playlist.update_track_count_and_duration_time(track.duration, increment=True)
            return Response({'detail': 'Track added to playlist.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid track ID.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_track(self, request, pk=None, track_id=None):
        playlist = self.get_object()

        if track_id:
            track = get_object_or_404(Track, id=track_id)
            existing_track = TrackInPlaylist.objects.filter(playlist=playlist, track=track).exists()

            if not existing_track:
                return Response({'detail': 'Track not exists.'}, status=status.HTTP_400_BAD_REQUEST)

            TrackInPlaylist.objects.get(playlist=playlist, track=track).delete()
            playlist.update_track_count_and_duration_time(track.duration, increment=False)
            return Response({'detail': 'Track deleted from playlist.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid track ID.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def tracks(self, request, pk=None):
        playlist = self.get_object()
        tracks_in_playlist = TrackInPlaylist.objects.filter(playlist=playlist)
        tracks = [track_in_playlist.track for track_in_playlist in tracks_in_playlist]

        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)
