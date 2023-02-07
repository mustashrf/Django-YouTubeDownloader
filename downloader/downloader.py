from pytube import YouTube , Playlist
import os
from zipfile import ZipFile
# import time

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
                    video.streams.get_audio_only().download(path + f'/{playlist_name}')
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
    
    video_name = video.title

    print("Downloading", video_name)
    if option == 'video':
        try:
            video.streams.get_by_resolution(quality).download(path)
        except:
            print(f'Download failed for {video_name}')
            return None

    elif option == 'audio':
        try:
            video.streams.get_audio_only().download(path)
        except:
            print(f'Download failed for {video_name}')
            return None

    msg = f'{video_name}: Downloaded!'
    print(msg)
    print('===============')
    return msg

def main(choice, input, ip):
    # PATH = f'Data/{str(round(time.time() * 1000))}'
    base_dir = 'Data'
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)

    PATH = f'{base_dir}/{ip}'
    if not os.path.isdir(PATH):
        os.makedirs(PATH)

    if choice == 'p':
        msg = downloadPlaylist(PATH, input)
        title = msg.split(':')[0]
        zipfilename = PATH + f'/{title}.zip'
        
        PATH += f'/{title}'
        if not os.path.isfile(zipfilename):
            files_list = os.listdir(PATH)

            if len(files_list) == 1:
                zipfilename = PATH + '/' + files_list[0]
            else:
                zipfile = ZipFile(zipfilename, 'w')
                for file in files_list:
                    zipfile.write(f'{PATH}/{file}', arcname=file)
        return msg, zipfilename
    
    elif choice == 's':
        msg = downloadSingleVideo(PATH, input)
        file = msg.split(':')[0]
        return msg, f'{PATH}/{file}'

    else:
        return None

def upgradePackage():
    stream = os.popen('pip install --upgrade pytube')
    output = stream.readlines()
        
