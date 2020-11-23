import pygauth, sys
from googleapiclient.discovery import build

creds = pygauth.get_user_creds_file('credentials.json', ['youtube'])
youtube = build('youtube', 'v3', credentials=creds)

print('getting playlist info')
resp = youtube.playlists().list(part='id,snippet', id=sys.argv[1]).execute()
source_playlist = resp['items'][0]

print('getting playlist videos')
resp = {'nextPageToken': None}
items = []
while 'nextPageToken' in resp:
    resp = youtube.playlistItems().list(part='snippet', playlistId=sys.argv[1], maxResults=50, pageToken=resp['nextPageToken']).execute()
    items.extend(resp['items'])

print('creating new playlist')
new_playlist = youtube.playlists().insert(part='id,snippet', body={
    'snippet': {
        'title': source_playlist['snippet']['title']
    }
}).execute()

print('adding new videos')
x = 0
for item in items:
    youtube.playlistItems().insert(part='snippet', body={
        'snippet': {
            'playlistId': new_playlist['id'],
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': item['snippet']['resourceId']['videoId']
            }
        }
    }).execute()
    x += 1
    print(f'\r{x}/{len(items)}', end='')