# mhyt


mhyt is a Python library for
downloading movies and music from youtube

mhyt can run in python 3+

## Examples
```python
from mhyt import yt_download
# download video and audio
url = "https://www.youtube.com/watch?v=0BVqFYParRs"
file = "Clouds.mp4"
yt_download(url,file)
#########################
# download music only
file = "Clouds_music.mp3"
yt_download(url,file,ismusic=True)
```
### Installing
to install with pip
type in terminal:
```
(sudo) pip install mhyt
```

## Built With
* [pydub](https://github.com/jiaaro/pydub) - for convert music
* [a-pytube-fork-for-spotdl-users](https://github.com/nficano/pytube) - to download files from youtube
* [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) - to download ffmpeg
## Author
**matan h**
## License
This project is licensed under the MIT License.

