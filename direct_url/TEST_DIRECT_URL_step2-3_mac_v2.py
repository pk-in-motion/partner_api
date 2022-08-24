#!/usr/bin/env python
import requests


#Authentication endpoint
auth_url = "https://partner.api.dailymotion.com/oauth/v1/token"


def get_access_token(client_id, client_secret):
    '''
    Authenticate on the API in order to get an access token
    '''

    response = requests.post(auth_url,
                             data={
                                 'client_id': client_id,
                                 'client_secret': client_secret,
                                 'grant_type': 'client_credentials',
                                 'scope': 'upload_videos read_videos edit_videos delete_videos'
                             },
                             headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             })

    if response.status_code != 200 or not 'access_token' in response.json():
        raise Exception('Invalid authentication response')

    return response.json()['access_token']


#Fill the client_id and client_secret generated in the step 1 and accessible directly from your Partner HQ.

access_token = get_access_token('....priv client id ....',
                                '....priv client secret.....')


#Creating a generic header with your access token
authorization_header = { 'Authorization' : 'Bearer ' +  access_token }




#Base endpoint to publish a video into your channel. The full url will looks like this: 'https://partner.api.dailymotion.com/rest/user/<your-channel-xid>/videos'
publish_video_url = 'https://partner.api.dailymotion.com/rest/user/'

#Now that your video file is uploaded, you can publish your video by setting it's mandatory fields
def publish_uploaded_video(channel_id ):
    '''
    Now that your video has been uploaded, you can publish it to make it visible
    '''

    publish_url = publish_video_url + channel_id + '/videos'
    uploaded_url_direct = 'https://storage.googleapis.com/dailymotion-support-sandbox/pk/test.mp4'

    response = requests.post(publish_url, data={
        "published": "true",
        "private": "true",
        "url": uploaded_url_direct,
        "title": "test",
        "channel": "videogames",
        "is_created_for_kids": "false"
    },
        headers= authorization_header )

    if response.status_code != 200 or not 'id' in response.json():
        raise Exception('Invalid publish video response')

    print(response.json())



#Calling the publish_uploaded_video function to set up the video mandatory fields and publish it into your channel
published_video = publish_uploaded_video('x24fekz')
