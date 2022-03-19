from http import client
from instagrapi import Client
from datetime import date
from time import sleep
from hashtags import get_hashtags
from datetime import datetime
import os

try:
    user_name = os.environ['USERNAME']
    password = os.environ['PASSWORD']
except:
    print("Issue with env!!!")
    sleep(60)
    exit()

filepath = "files/upload.mp4"
thumbpath = "files/thumb.jpg"
db_file = "files/last_uploaded_on.txt"
fu_file = "files/first_upload_on.txt"


def get_today():
    return date.today()

def write_today_to_file():
    f = open(db_file, "w")
    f.write(str(get_today()))
    f.close()

def check_if_done_for_today():
    try:
        f = open(db_file, "r")
    except:
        print("Issue with the last date file!")
        sleep(5)
        exit()

    return (f.read() == str(get_today()))

def get_day_num():
    try:
        f = open(fu_file, "r")
        content = f.read()
        if(content == ""):
            f = open(fu_file, "w")
            f.write(str(get_today()))
            return 1
        else:
            datetime_object = datetime.strptime(content)
            return (get_today() - datetime_object.date()).days + 1
    except Exception as e:
        print("Issue with the first upload file!", e)
        sleep(5)
        exit()

def uploadReel(api, path):
    daynum = get_day_num()
    print(f"\nUploading Reel for day {daynum}...")
    hashtags = get_hashtags("marvel")
    api.video_upload(path, f"Day {daynum} \n\n{hashtags} @midhunvnadh", thumbpath, [], "", extra_data = {})
    write_today_to_file()
    print("Done!\n")

def startApi():
    cl = Client()
    print(f"Logging in {user_name}...")
    try:
        cl.login(user_name, password)
    except:
        print("Couldn't login... try again in an hour")
        sleep(60 * 60)
        exit() # Docker will reboot the container
    while True:
        try:
            if not check_if_done_for_today():
                uploadReel(cl, filepath)
        except Exception as e:
            print(e)
            print("Program Quitted...")

        sleep(60 * 60)

startApi()