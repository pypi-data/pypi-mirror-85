from __future__ import unicode_literals

__all__ = "yt_download"

import os




def yt_download(url, filename=None, ismusic=False, video_format=None, **ydl_opts):
    import youtube_dl
    import os
    if video_format is None:
        video_format = os.path.splitext(filename)[1][1:]
    if not ismusic:
        ydl_opts["format"] = video_format
    if ismusic:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': video_format,
                'preferredquality': '192'
            }],
            'postprocessor_args': [
                '-ar', '16000'
            ],
            'prefer_ffmpeg': True,
        }
    if filename is not None:
        ydl_opts["outtmpl"] = filename
        ##########################
        music_messege = "as music"
    else:
        music_messege = ""
    print(f"download {url} in format {video_format} in file {filename} {music_messege}")
    ########
    ydl_opts.update(ydl_opts)
    #############################################
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def _get_ffmpeg_path():
    err = os.system("ffmpeg -version")
    if err == 0:  # ffmpeg in path
        ffmpeg = "ffmpeg"
    else:  # not in Path
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    ffmpeg = '\"' + ffmpeg + '\"'
    return ffmpeg