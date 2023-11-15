import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pandas import json_normalize

class YouTubeApi:
    def __init__(self):
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "client_secret.json"
        self.scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes)
        self.credentials = flow.run_local_server(port=5001)
        self.regionCode = "CA"

    def GetVideoCategories(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=self.credentials)

        request = youtube.videoCategories().list(
            part="snippet",
            regionCode="CA"
        )
        response = request.execute()
        return response

    def GetMostPopularVideos(self, categoryId, numResults):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=self.credentials)
        
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            maxResults=numResults,
            regionCode=self.regionCode,
            videoCategoryId=categoryId
        )
        response = request.execute()
        return response
