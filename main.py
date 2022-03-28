from pytube import YouTube
from moviepy.editor import *
import os
import PySimpleGUI as sg


def gui():
    # colors
    sg.theme('sandy beach')
    # general layout
    layout = [
        [sg.Text('Enter the YouTube link')],
        [sg.Text('Link', size=(15, 1)), sg.InputText()],
        [sg.Submit('MP4'), sg.Submit('MP3'), sg.Button('Cancel')]
    ]

    window = sg.Window("Omid's YouTube Downloader", layout)
    event, values = window.read()
    window.close()

    # check to see if it's a link
    if values[0].lower().startswith(("https://www.youtube.com/watch", "https://www.youtu.be/watch")):
        # if it's a link, assign it to yt
        global yt
        yt = YouTube(values[0])
        if event == 'MP4':
            mp4_maker()
            sys.exit()
        if event == 'MP3':
            mp4_maker_temp()
            mp3_maker()
            sys.exit()
    # on cancel, exit, no matter if link or no link
    elif event == 'Cancel':
        sys.exit()

    # if it's not a link, then start again
    else:
        sg.Popup('Please enter a valid URL!', keep_on_top=True)
        gui()


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
    """TODO check for file duplicate. If the file exist, then it is renamed."""
    ys = yt.streams.get_highest_resolution()
    ys.download()
    # rename the title of the video.mp to tmp.mp4
    os.rename(yt.title + '.mp4', 'tmp.mp4')


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
        os.rename('tmp.mp4', yt.title + '.mp4')
        sys.exit()


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


gui()
