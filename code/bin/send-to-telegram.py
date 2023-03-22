#!/usr/bin/python

import requests
from time import sleep
import argparse
from datetime import datetime
import os.path
import json
import base64

script_dir = os.path.dirname(__file__)
credentials_file_path = os.path.join(script_dir, "../cfg/telegram/credentials.json")
# print(credentials_file_path)

with open(credentials_file_path) as credentials_file:
    credentials = json.load(credentials_file)

apiToken = credentials['apiToken']
chatID = credentials['chatID']
# print("apiToken =", apiToken)
# print("chatID =", chatID)

peepcam_local_url = credentials['peepcam_local_url']
peepcam_external_url = credentials['peepcam_external_url']

apiURL = f'https://api.telegram.org/bot{apiToken}/'

def parse_command_line():

    parser = argparse.ArgumentParser(description='Send push notifcations to telegram')
    parser.add_argument('-n', '--note',    help='Send a custom note')
    parser.add_argument('-p', '--picture', help='Send a picture')
    parser.add_argument('-v', '--video',   help='Send a video')
    args = parser.parse_args()

    return args


def send_message(message):

    try:
        response = requests.post(apiURL + "sendMessage", json={'chat_id': chatID, 'text': message, 'parse_mode': "MarkdownV2"})
        print(response.text)
    except Exception as e:
        print(e)


def send_image(picture_file):

    params = {'chat_id': chatID}
    files = {'photo': picture_file}

    try:
        response = requests.post(apiURL + "sendPhoto", params, files=files)
        print(response.text)
    except Exception as e:
        print(e)


def send_video(video_file):

    params = {'chat_id': chatID}
    files = {'video': video_file}

    try:
        response = requests.post(apiURL + "sendVideo", params, files=files)
        print(response.text)
    except Exception as e:
        print(e)



if __name__ == "__main__":

    args = parse_command_line()

    now = datetime.now()
    date = now.strftime("%d/%m")
    time = now.strftime("%Hh%M")

    if not args.video and not args.picture and not args.note:

        print("Pushing a note")
        send_message("{} {} *Motion detect*\n[Local URL]({}) \| [External URL]({})".format(
            date, time, peepcam_local_url, peepcam_external_url))

    else:

        if args.note:
            print("Pushing a custom note")
            print("> {}".format(args.note))
            title = "Custom Note"
            send_message("{}".format(args.note))

        elif args.picture:
            file_path = args.picture
            with open(file_path, mode='rb') as file:
                img = file.read()
            print("Sending picture {}".format(file_path))
            send_image(img)

        elif args.video:
            file_path = args.video
            with open(file_path, mode='rb') as file:
                video = file.read()
            print("Sending video {}".format(file_path))
            send_video(video)

        else:
            print("File path is missing")
            exit(1)
