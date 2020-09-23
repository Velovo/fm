from playsound import playsound
import twitter as tw
import requests
import os
import sys
import random
import string
import json
import time
import eyed3
import multiprocessing

token_filename = 'token.json'

token = json.load(open(token_filename, 'r'))

api = tw.Api(consumer_key=token['consumer_key'],
            consumer_secret=token['consumer_secret'],
            access_token_key=token['access_token_key'],
            access_token_secret=token['access_token_secret'])

def random_string(length):
    letters = string.ascii_lowercase
    return (''.join(random.choice(letters) for i in range(length)))

def test_string(strr):
    for i in strr:
        if i.isalnum() or i == '-' or i == '?' or i == '=' or i == '_':
            pass
        else:
            return 1
    return 0

def t_play(filename):
    playsound(filename + '.mp3')
    print('Finished audio\ndeleting file')
    os.remove(filename + '.mp3')

def t_download(filename, url):
    if url.startswith('https://youtu.be/') and test_string(url.split('https://youtu.be/')[1]) == 0:
        print('Starting youtube-dl')
        os.system('youtube-dl --extract-audio --audio-format mp3 -o "' + filename + '.%(ext)s" ' + url)
        print('Can\'t get metadata trough youtube\nFinished downloading, now playing')
    elif url.startswith('https://open.spotify.com/track/') and test_string(url.split('https://open.spotify.com/track/')[1]) == 0:
        print('Starting spotdl')
        os.system('spotdl -o mp3 -f' + filename + '.mp3 --song ' + url)
        c_file = eyed3.load(filename + '.mp3')
        print('Finished downloading\nTitle:  ' + c_file.tag.title + '\nArtist: ' + c_file.tag.artist)

def geturl_twitter():
    i = 0
    url = None

    print('Getting url')
    i = 0
    ret = api.GetSearch(raw_query='q=open.spotify.com&result_type=recent&count=10')
    while i < 10 and url == None:
        try:
            url = ret[i].urls[0].expanded_url
            if not url.startswith('https://open.spotify.com/track/'):
                url = None
        except:
            pass
        i = i + 1
    return url

def geturl():
    url = None

    while url == None:
        url = geturl_twitter()
        if url == None:
            time.sleep(10)
    return (url)

def get_input():
    inp = None
    while (inp == None):
        try:
            inp = input('&> ').split(' ')
        except:
            pass
    if inp[0] == 'play' and len(inp) != 2:
        return (None)
    if inp[0] == 'stop' and len(inp) != 1:
        return (None)
    if inp[0] == 'radio' and len(inp) != 1:
        return (None)
    if inp[0] == 'delete' and len(inp) != 1:
        return (None)
    if inp[0] == 'exit' and len(inp) != 1:
        return (None)
    return inp

def play(filename, inp, p):
    p = multiprocessing.Process(target=t_download, args=(filename, inp[1],))
    p.start()
    p.join()
    p = multiprocessing.Process(target=t_play, args=(filename,))
    p.start()
    return (p)

def stop(p):
    try:
        p[0].terminate()
    except:
        pass

def delete():
    ls = os.listdir(os.getcwd())
    print('This will erase all the mp3 file from this directory: ' + os.getcwd())
    inp = input('continue ? (y/n)')
    if inp == 'y':
        for files in ls:
            if files.endswith('.mp3'):
                os.remove(os.path.join(os.getcwd(), files))

def radio():
    while (True):
        url = geturl()
        filename = random_string(32)
        t_download(filename, url)
        t_play(filename)

def start_radio():
    p = list()

    p.append(None)
    p[0] = multiprocessing.Process(target=radio, args=())
    p[0].start()
    p.append(None)
    return (p)

def main():
    url = None
    p = list()

    p.append(None)
    while (True):
        inp = None
        if len(p) == 2:
            p[1] = random_string(32)
        else:
            p.append(random_string(32))
        while inp == None:
            inp = get_input()
        if inp[0] == 'play':
            stop(p)
            p[0] = play(p[1], inp, p[0])
        if inp[0] == 'stop':
            stop(p)
        if inp[0] == 'radio':
            stop(p)
            p = start_radio()
        if inp[0] == 'delete':
            delete()
        if inp[0] == 'exit':
            stop(p)
            sys.exit()

if __name__ == "__main__":
    main()
