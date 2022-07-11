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
