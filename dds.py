#!/usr/bin/env python

import requests, os, shutil, subprocess

auth_url = 'https://www.deviantart.com/oauth2/token'

auth_post_body = {
    'grant_type': 'client_credentials',
    'client_id': os.environ['CLIENT_ID'],
    'client_secret': os.environ['CLIENT_SECRET']
}

auth_json = requests.post(auth_url, auth_post_body).json()
access_token = auth_json['access_token']

dd_url = 'https://www.deviantart.com/api/v1/oauth2/browse/dailydeviations?access_token=' + access_token
dd_json = requests.get(dd_url).json()

if os.path.exists('./deviations'):
    shutil.rmtree('./deviations')
os.mkdir('./deviations')

file_count = 0

for deviation in dd_json['results']:
    if 'content' in deviation:
        image = requests.get(deviation['content']['src'])
        filename = './deviations/' + str(file_count) + '.jpg'
        open(filename, 'wb').write(image.content)
        file_count += 1

subprocess.run('fbi -noverbose -a -t 10 ./deviations/*.jpg', shell=True)
