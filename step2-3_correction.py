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
access_token = get_access_token('<Your-client-id>',
                                '<Your-client-secret>')


#Using the function from the step above to retrieve an access_token. (The function is not present in this document to keep it simple)
access_token = get_access_token('<Your-client-id>',
                         '<Your-client-secret>')

#Creating a generic header with your access token
authorization_header = { 'Authorization' : 'Bearer ' +  access_token }




#Endpoint to retrieve an upload URL
file_upload_url = 'https://partner.api.dailymotion.com/rest/file/upload'

#Getting an upload url to upload the video file
def get_upload_url():
    '''
    Getting an upload url be able to store your video file
    '''
    response = requests.get(url=file_upload_url,
                            headers= authorization_header )

    if response.status_code != 200 or not 'upload_url' in response.json():
        raise Exception('Invalid upload url response')

    return response.json()['upload_url']




#Sending the video file to the upload url obtained in the previous function
def upload_video_file(url):
    '''
    Uploading your video file to the platform
    '''

    files = {'file': open(
        'Path/To/Your/File', 'rb')}

    response = requests.post(url,
                             files=files,
                             headers= authorization_header)

    if response.status_code != 200 or not 'url' in response.json():
        raise Exception('Invalid upload video file response')

    return response.json()['url']




#Base endpoint to publish a video into your channel. The full url will looks like this: 'https://partner.api.dailymotion.com/rest/user/<your-channel-xid>/videos'
publish_video_url = 'https://partner.api.dailymotion.com/rest/user/'

#Now that your video file is uploaded, you can publish your video by setting it's mandatory fields
def publish_uploaded_video(uploaded_url, channel_id ):
    '''
    Now that your video has been uploaded, you can publish it to make it visible
    '''

    publish_url = publish_video_url + channel_id + '/videos'

    response = requests.post(publish_url, data={
        "published": "true",
        "url": uploaded_url,
        "title": "YourVideoTitle",
        "channel": "videogames",
        "is_created_for_kids": "false"
    },
        headers= authorization_header )

    if response.status_code != 200 or not 'id' in response.json():
        raise Exception('Invalid publish video response')

    #return response.json()
    print(response.json())


#Executing the functions:

#Calling the get_upload_url function to retrieve the file upload url
upload_url = get_upload_url()
#upload_url = get_upload_url( authorization_header )
#TypeError: get_upload_url() takes 0 positional arguments but 1 was given


#Calling the upload_video_file function to upload the video file
uploaded_url = upload_video_file(upload_url)
# uploaded_url = upload_video_file(upload_url,  authorization_header )
# TypeError: upload_video_file() takes 1 positional argument but 2 were given


#Calling the publish_uploaded_video function to set up the video mandatory fields and publish it into your channel
published_video = publish_uploaded_video(uploaded_url, <your-channel-xid>)
