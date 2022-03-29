"""This is WIP!"""

from pytube import YouTube
from moviepy.editor import *
import os


def choice_question():
    while True:
        choice = input("MP4 or MP3? ")
        if choice.lower() == 'mp4':
            mp4_maker()
            break
        if choice.lower() == 'mp3':
            mp4_maker()
            mp3_maker()
            break
        else:
            print('Enter a valid format!')


def link_taker():
    # take the link
    link = input('Enter the link: ')
    if link.lower().startswith(("https://www.youtube.com/watch", "https://www.youtu.be/watch")):
        global yt
        yt = YouTube(link)
    else:
        print("Please enter a valid link!")
        link_taker()


def info_spit():
    # spit it out
    print("Title: ", yt.title)
    print("Description: ", yt.description)
    print("Length: ", yt.length)


def mp4_maker():
    # print(yt.streams.filter(only_audio=True))
    ys = yt.streams.get_highest_resolution()
    ys.download()


def mp4_maker_temp():
    ys = yt.streams.get_highest_resolution()
    ys.download(filename='tmp.mp4')
    # rename the title of the video.mp to tmp.mp4
    # os.rename(yt.title + '.mp4', 'tmp.mp4')


# TODO make cli based mp3_maker
def mp3_maker():
    # grab the title
    title = yt.title
    # it is the temporary file
    mp4_file = 'tmp.mp4'
    mp3_file = title + '.mp3'
    # convert it
    videoclip = VideoFileClip(mp4_file)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)
    # make it pretty
    audioclip.close()
    videoclip.close()
    # ask and delete mp4
    layout = [
        [sg.Text('Should I delete the MP4?')],
        [sg.Submit('Yes'), sg.Submit('No')]
    ]
    window = sg.Window("Omid's YouTube Downloader", layout)
    event, values = window.read()
    window.close()

    if event == 'Yes':
        os.remove('tmp.mp4')
    if event == 'No':
        # rename tmp.mp4 to title if user wants to keep both mp4 and mp3.
        if os.path.isfile(yt.title + '.mp4'):
            for i in range(1, 10000):
                # if file duplicate with number exists, make a new one with number + 1
                if os.path.isfile(yt.title + ' ' + str(i) + '.mp4'):
                    os.rename('tmp.mp4', yt.title + ' ' + str(i + 1) + '.mp4')
                    sys.exit()
                # if file already exists, add a number to the end of it
                else:
                    os.rename('tmp.mp4', yt.title + ' ' + str(i) + '.mp4')
                    sys.exit()
        # rename the temporary file to the YouTube title

        # TODO also rename numbered tmp.mp4 files
        else:
            os.rename('tmp.mp4', yt.title + '.mp4')
            sys.exit()
