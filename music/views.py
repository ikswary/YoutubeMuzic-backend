import os

from django.http import StreamingHttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from pydub import AudioSegment

from .models import Media


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
