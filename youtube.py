import io
from colorama import init, Fore
from pytube import YouTube


def get_yt_video(url: str) -> io.BytesIO:
    buffer = io.BytesIO()
    url_ = YouTube(url)
    resolutions = url_.streams.filter(file_extension='mp4', progressive=True).order_by('resolution')
    used_res = []
    for res in resolutions[::-1]:
        if res.resolution not in used_res:
            used_res.append(res.resolution)
            if res.filesize < 50000000:
                size = f"Downloading video in {res.resolution} resolution ({round(float(res.filesize / 1000000), 2)} MB)"
                resolution = res
                break

    itag = resolution.itag
    video = url_.streams.get_by_itag(itag)
    video.stream_to_buffer(buffer)
    buffer.seek(0)

    return buffer, size


def get_yt_sound(url: str) -> io.BytesIO:
    buffer = io.BytesIO()
    url_ = YouTube(url)
    sounds = url_.streams.filter(only_audio=True)
    used_sounds = []
    for sound in sounds[::-1]:
        if sound.abr not in used_sounds:
            used_sounds.append(sound.abr)
            if sound.filesize < 50000000:
                size = f"Downloading sound in {sound.abr} ({round(float(sound.filesize / 1000000), 2)} MB)"
                sound_ = sound
                break
    
    itag = sound_.itag
    sound = url_.streams.get_by_itag(itag)
    sound.stream_to_buffer(buffer)
    buffer.seek(0)

    return buffer, size