import pygauth, sys
from googleapiclient.discovery import build

if len(sys.argv) == 1:
    print('Please provide a channel id')
    exit()

creds = pygauth.get_user_creds_file('credentials.json', ['youtube'])
youtube = build('youtube', 'v3', credentials=creds)

resp = {'nextPageToken': None}
items = []
x = 0
while 'nextPageToken' in resp:
    resp = youtube.search().list(part='id', channelId=sys.argv[1], maxResults=50, pageToken=resp['nextPageToken'], type='video', safeSearch='none').execute()
    x += len(resp['items'])
    items.extend(resp['items'])
    print(f'\r{x} videos found', end='')

print('\nvideo ids:\n')

for item in items:
    print(item['id']['videoId'])