import os
import json
import random

from django.http      import StreamingHttpResponse, HttpResponse, JsonResponse
from django.views     import View
from django.shortcuts import get_object_or_404
from django.db.models import F
from pydub            import AudioSegment

from .models          import (
    Collection,
    Playlist,
    Media,
    Artist,
    Type,
    Thumbnail,
    Hotlist
)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize, length=0):
        self.filelike = filelike
        self.blksize = blksize
        self.remaining = length

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


class StreamView(View):
    MILISECOND_TO_SECOND = 1000

    def get(self, request, media_id):
        audio_source = get_object_or_404(Media,id=media_id).url
        audio = AudioSegment.from_mp3(audio_source)
        playtime = len(audio) / self.MILISECOND_TO_SECOND
        size = os.path.getsize(audio_source)
        bytes_per_sec = int(size / playtime)

        resp = StreamingHttpResponse(RangeFileWrapper(open(audio_source, 'rb+'), bytes_per_sec * 10, size),
                                     status=200, content_type='audio/mp3')
        resp['Cache-Control'] = 'no-cache'
        return resp


class MainView(View):
    BASIC_COLLECTION_IDS = [1, 7, 13]
    VARIABLE_COLLECTIONS = [3 ,4, 8, 10, 12, 15]

    def get(self, request):
        range_list = request.GET.getlist('collection_id')
        if not range_list:
            range_list = self.BASIC_COLLECTION_IDS

        collection = Collection.objects.prefetch_related('playlist_set')

        payload = {
                'contents': [{
                    'collection':collection.filter(id=i).values('name').first()['name'],
                    'elements': list(
                        collection.filter(id=i).annotate(
                            list_id     = F('playlist__id'),
                            list_name   = F('playlist__name'),
                            list_thumb  = F('playlist__thumbnail_id__url'),
                            list_type   = F('playlist__type_id__name'),
                            list_artist = F('playlist__artist')
                        ).values(
                            'list_id',
                            'list_name',
                            'list_thumb',
                            'list_type',
                            'list_artist'
                        ))
                    } for i in range_list ]}

        def get_metadata(payload):
            payload['main_thumb']= collection.filter(
                name = payload['contents'][0]['collection']
            ).values('thumbnail_id__url').first()['thumbnail_id__url']

            payload['range_list']=random.sample(self.VARIABLE_COLLECTIONS, 6)
            return

        if not request.GET :
            get_metadata(payload)

        return JsonResponse(payload, status=200)
