from pytube import YouTube , Playlist
import os
from zipfile import ZipFile
import time

def getExceptions(str):

    exceptions = []

    str = str.split(',')
    for s in str:
        if s.__contains__('-'):
            s = s.split('-')
            exceptions += range(int(s[0]), int(s[-1])+1)
        else:
            exceptions.append(int(s))

    print(exceptions)
    return exceptions

def downloadPlaylist(path, input):
    url = input[0]

    option = input[1]
    quality = input[2]

    exception = input[3]
    if exception != '':
        exception = getExceptions(exception)
    else:
        exception = []

    playlist = Playlist(url)
    
    length_of_exception = len(exception)
    playlist_range = range(1, len(playlist.video_urls)+1) if length_of_exception == 0 else exception

    playlist_length = len(playlist_range)
    print(f"{playlist_length} video(s)")
    playlist_name = playlist.title

    i = 1
    d = 0

    if option == 'video':
        for video in playlist.videos:
            
            if i in playlist_range:
                try:
                    print("Downloading {}".format(video.title))
                    v = video.streams.get_by_resolution(quality)

                    if v is None:
                        v = video.streams.get_highest_resolution()
                    
                    v.download(path)

                    d+=1
                except:
                    print(f'Download failed for {video.title}')
                    continue

            i += 1
    
    elif option == 'audio':
        for video in playlist.videos:
            
            if i in playlist_range:
                try:
                    print("Downloading {}".format(video.title))
                    video.streams.get_audio_only().download(path)
                    d+=1
                except:
                    print(f'Download failed for {video.title}')
                    continue
            i += 1

    if d == 0:
        return None

    msg = f"{playlist_name}: Downloaded {d} of {playlist_length}"
    print(msg)
    print('===============')
    return msg
        
def downloadSingleVideo(path, input):

    msg = ''
    link = input[0]
    option = input[1]
    quality = input[2]

    video = YouTube(link)
    
    print("Downloading",video.title)
    if option == 'video':
        try:
            video.streams.get_by_resolution(quality).download(path)
        except:
            print(f'Download failed for {video.title}')
            return None

    elif option == 'audio':
        try:
            video.streams.get_audio_only().download(path)
        except:
            print(f'Download failed for {video.title}')
            return None

    msg = 'Downloaded!'
    print(msg)
    print('===============')
    return msg

def main(choice, input, ip):

    upgradePackage()

    # PATH = f'Data/{str(round(time.time() * 1000))}'
    root = 'Data'
    if not os.path.isdir(root):
        os.makedirs(root)

    PATH = f'{root}/{ip}'
    if not os.path.isdir(PATH):
        os.makedirs(PATH)

    if choice == 'p':
        msg = downloadPlaylist(PATH, input)
    
    elif choice == 's':
        msg = downloadSingleVideo(PATH, input)

    if msg:
        files_list = os.listdir(PATH)
        if len(files_list) == 1:
            file = files_list[0]
            return msg, f'{PATH}/{file}'

        elif len(files_list) > 1:
            name = msg.split(':')[0]
            filename = PATH + f'/{name}.zip'
            if not os.path.isfile(filename):
                zipfile = ZipFile(filename, 'w')
                for file in files_list:
                    zipfile.write(f'{PATH}/{file}', arcname=file)
            return msg, filename

    else:
        return None

def upgradePackage():
    stream = os.popen('pip install --upgrade pytube')
    output = stream.readlines()
        
