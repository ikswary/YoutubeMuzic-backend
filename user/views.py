import json
import requests
import jwt

from django.http import HttpResponse, JsonResponse
from django.views import View

from YoutubeMuzic.settings import SECRET_KEY
from music.models import (
    Media,
    Playlist
)
from .models import (
    User,
    RecentMedia,
    RecentPlaylist,
    Evaluation
)
from .utils import login_required


class GoogleSignInView(View):
    GOOGLE_AUTH_URL = 'https://oauth2.googleapis.com/tokeninfo?id_token='
    CORRECT_ISS_LIST = ['accounts.google.com', 'https://accounts.google.com']

    def post(self, request):
        try:
            data = json.loads(request.body)
            google_id = data['id']
            google_token = data['token']
            token_data = json.loads(requests.get(self.GOOGLE_AUTH_URL + google_token).text)

            if (token_data['iss'] not in self.CORRECT_ISS_LIST) or (
                    token_data['sub'] != google_id):
                return JsonResponse({'message': 'MODIFIED_TOKEN'}, status=401)

            user, created = User.objects.get_or_create(google_id=google_id)
            token = jwt.encode(
                {'id': user.id}, SECRET_KEY, 'HS256'
            ).decode('utf-8')
            return JsonResponse({'token': token}, status=200)

        except KeyError:
            return HttpResponse(status=400)


class RecentMediaView(View):
    @login_required
    def post(self, request, user):
        try:
            media_id = json.loads(request.body)['media_id']
            media = Media.objects.get(id=media_id)
            recent_playlist, created = RecentMedia.objects.get_or_create(user=user, media=media)
            if not created:
                recent_playlist.save()

            return HttpResponse(status=200)

        except KeyError:
            return HttpResponse(status=400)
        except ValueError:
            return HttpResponse(status=400)
        except Media.DoesNotExist:
            return HttpResponse(status=404)


class RecentPlaylistView(View):
    LIMIT = 19

    @login_required
    def post(self, request, user):
        try:
            playlist_id = json.loads(request.body)['playlist_id']
            playlist = Playlist.objects.get(id=playlist_id)
            recent_playlist, created = RecentPlaylist.objects.get_or_create(user=user, playlist=playlist)
            if not created:
                recent_playlist.save()

            return HttpResponse(status=200)

        except KeyError:
            return HttpResponse(status=400)
        except ValueError:
            return HttpResponse(status=400)
        except Playlist.DoesNotExist:
            return HttpResponse(status=404)

    @login_required
    def get(self, request, user):
        try:
            user = User.objects.prefetch_related('recentplaylist_set__playlist').get(id=user.id)
            recent_playlists = user.recentplaylist_set.select_related(
                'playlist__thumbnail', 'playlist__type').order_by(
                '-listened_at')[:self.LIMIT]
            element_list = list()

            for recent_playlist in recent_playlists:
                element = {
                    'list_id': recent_playlist.playlist.id,
                    'list_name': recent_playlist.playlist.name,
                    'list_thumb': recent_playlist.playlist.thumbnail.url,
                    'list_artist': recent_playlist.playlist.artist
                }
                if recent_playlist.playlist.type:
                    element['list_type'] = recent_playlist.playlist.type.name
                if not recent_playlist.playlist.type:
                    element['list_type'] = 'Null'
                element_list.append(element)

            response = {
                'collection': "최근 재생",
                'elements': element_list
            }

            return JsonResponse({"contents": response}, status=200)

        except KeyError:
            return HttpResponse(status=400)

class LikeMusicView(View):
    @login_required
    def get(self, request, user):
        user = User.objects.prefetch_related('evaluation_set__media').get(id=user.id)
        liked_medias = user.evaluation_set.filter(like=True).select_related(
            'media__thumbnail', 'media__artist')

        response = [
            {
                'item_id': liked_media.media.id,
                'item_thumb': liked_media.media.thumbnail.url,
                'item_name': liked_media.media.name,
                'item_artist': liked_media.media.artist.name,
                'item_album': liked_media.media.album,
                'item_length': liked_media.media.length
            }
            for liked_media in liked_medias]

        return JsonResponse({'contents': response}, status=200)

class EvaluationView(View):
    @login_required
    def post(self, request, user):
        try:
            media_id, like = json.loads(request.body).values()
            media = Media.objects.get(id=int(media_id))

            evaluation, created = Evaluation.objects.get_or_create(
                user=user,
                media=media
            )
            if not created and evaluation.like == like:
                evaluation.delete()
                return JsonResponse({'like': None}, status=200)

            evaluation.like = like
            evaluation.save()

            return JsonResponse({'like': like}, status=200)

        except ValueError:
            return HttpResponse(status=400)
        except json.decoder.JSONDecodeError:
            return HttpResponse(status=400)

    @login_required
    def get(self, request, user):
        try:
            media_id = request.GET['media_id']
            evaluation = Evaluation.objects.get(user=user, media_id=media_id)
            return JsonResponse({'like': evaluation.like}, status=200)

        except KeyError:
            return HttpResponse(status=400)
        except ValueError:
            return HttpResponse(status=400)
        except Evaluation.DoesNotExist:
            return JsonResponse({'like': None}, status=200)
