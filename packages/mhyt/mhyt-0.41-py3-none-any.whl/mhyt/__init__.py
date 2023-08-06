from __future__ import unicode_literals

__all__ = "yt_download"

import os
import shutil
import pytube.query
from pytube import YouTube
import pytube
from pydub import AudioSegment


def yt_download(url, filename=None, ismusic=False, video_format=None, choose=pytube.query.StreamQuery.first,
                overwrite=True, **filter_opts):
    if not filter_opts:
        filter_opts = dict(only_audio=ismusic)
    if "only_audio" not in filter_opts.keys():
        filter_opts.update(dict(only_audio=ismusic))
    yt = YouTube(url).streams.filter(only_audio=True,mime_type="audio/webm")


    if os.path.exists(".mhyt-tmp\\a.mp4"):
        os.remove(".mhyt-tmp\\a.mp4")
    a = choose(yt).download(".mhyt-tmp", filename="a")
    if os.path.exists(filename):
        if overwrite:
            os.remove(filename)
        else:
            raise FileExistsError("the file \"{}\" has exists".format(filename))
    os.rename(a, filename)
    #################################
    if ismusic:
        if not video_format == None:
            as1 = AudioSegment.from_mp3(filename)
            as1.export(filename, format=video_format)
        else:
            as1= AudioSegment.from_file(filename,"webm")
            as1.export(filename,"mp3")
        # # #
    if os.path.exists(".mhyt-tmp\\a.mp4"):
        os.remove(".mhyt-tmp\\a.mp4")
    if os.path.exists(".mhyt-tmp\\a.webm"):
        os.remove(".mhyt-tmp\\a.webm")

    if os.path.exists(".mhyt-tmp"):
        shutil.rmtree(".mhyt-tmp",ignore_errors=True,onerror=print)

    print(f"done download {url} to file {filename}")


def _get_ffmpeg_path():
    err = os.system("ffmpeg -version")
    if err == 0:  # ffmpeg in path
        ffmpeg = "ffmpeg"
    else:  # not in Path
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    ffmpeg = '\"' + ffmpeg + '\"'
    return ffmpeg


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=0BVqFYParRs"
    #########################
    file = "Clouds_music.mp3"
    yt_download(url, file,ismusic=True)