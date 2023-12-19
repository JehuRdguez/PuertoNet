from django.conf import settings
import requests
import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import google.auth


def title_formatting(title):

	if len(title) >= 30:
		return f'{title[0:26]}...'
	else:
		return title



'''
Retreives video data from a YouTube channel
'''
class YouTube:

	def __init__(self, *args, **kwargs):

		#vid_id for get_video
		self.vid_id = kwargs.get("vid_id")

		self.api_service_name = settings.API_SERVICE_NAME #This is 'youtube' for this tutorial
		self.api_version = settings.API_VERSION #This is 'v3' for this tutorial
		self.developer_key = settings.GOOGLE_API_KEY # make sure you have Youtube APIS enabled in Google console
		self.channel_id = settings.CHANNEL_ID # This will be your own channel ID for this tutorial


		self.youtube = googleapiclient.discovery.build(
	        self.api_service_name,
	        self.api_version,
	        developerKey=self.developer_key
	        )

	def get_data(self):


		#get playlists for channelId
		playlist_request = self.youtube.playlists().list(
			part="snippet,contentDetails",
			channelId=self.channel_id,
			)
		
		playlist_response = playlist_request.execute()

		#list of playlists
		playlists = [p["id"] for p in playlist_response["items"]]

		nextPageToken = None

		videos = []
		data = []
		
		while True:
			
			#make another request for playlist data (max results for page 1 is 50) 
			for pl in playlists:
				playlist_items_request = self.youtube.playlistItems().list(
					part="contentDetails",
					playlistId=pl,
					maxResults=50,
					pageToken=nextPageToken
					)
				playlist_items_response = playlist_items_request.execute()

				#append video ID to list
				for item in playlist_items_response["items"]:
					videos.append(item["contentDetails"]["videoId"])
			
			#make another request to get video specific infomation
			video_request = self.youtube.videos().list(
				part="contentDetails,snippet,player",
				id=",".join(videos)
				)
			video_response = video_request.execute()

			for item in video_response["items"]:

				#create dict for each video and append to data list
				vid_data = {
					"id": item["id"],
					"title":item["snippet"]["title"],
					"title_formatted":title_formatting(item["snippet"]["title"]),
					"description":item["snippet"]["description"],
					"thumbnail":item["snippet"]["thumbnails"]["medium"]["url"],
					"iframe":item["player"]["embedHtml"],
					"categoria":item["snippet"]["tags"],
					"fecha":item["snippet"]["publishedAt"],
					"duracion":item["contentDetails"]["duration"],

				}

				data.append(vid_data)

			
			#get next page token from request - break while loop if there aren't anymore pages
			nextPageToken = playlist_response.get("nextPageToken")
			if not nextPageToken:
				break

		return data

	def get_video(self):


		#retrieve data for 1 x video. This is similar to the get_data method	
		video_request = self.youtube.videos().list(
			part="contentDetails,snippet,player",
			id=self.vid_id
			)
		
		video_response = video_request.execute()

		item = video_response["items"][0]
		vid_data = {
			"id": item["id"],
			"title":item["snippet"]["title"],
			"description":item["snippet"]["description"],
			"iframe":item["player"]["embedHtml"],
			"categoria":item["snippet"]["tags"],
			"fecha":item["snippet"]["publishedAt"],
			"duracion":item["contentDetails"]["duration"],
		}

		return vid_data



class YouTubeUploader:
    def __init__(self, api_name, api_version, client_secrets_path, credentials_path, channel_id, *args, **kwargs):
        self.api_name = api_name
        self.api_version = api_version
        self.client_secrets_path = client_secrets_path
        self.credentials_path = credentials_path
        self.channel_id = channel_id
        self.youtube = self.build_service()


    def build_service(self):
        credentials = self.get_credentials()
        return build(self.api_name, self.api_version, credentials=credentials)

    def get_credentials(self):
        credentials = None

        if os.path.exists(self.credentials_path):
            credentials = Credentials.from_authorized_user_file(self.credentials_path)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_path, ['https://www.googleapis.com/auth/youtube.upload']
                )
                credentials = flow.run_local_server(port=0)

            with open(self.credentials_path, 'w') as credentials_file:
                credentials_file.write(credentials.to_json())

        return credentials

    def upload_video(self, video_path, title, description, tags=None, category_id=None):
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category_id,
            },
            'status': {
                'privacyStatus': 'private',
            },
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

        response = self.youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        ).execute()

        return response










class YouTubeApi:
    def __init__(self, *args, **kwargs):
        self.vid_id = kwargs.get("vid_id")
        self.api_service_name = settings.API_SERVICE_NAME
        self.api_version = settings.API_VERSION
        self.developer_key = settings.GOOGLE_API_KEY
        self.channel_id = settings.CHANNEL_ID

        self.youtube = googleapiclient.discovery.build(
            self.api_service_name,
            self.api_version,
            developerKey=self.developer_key
        )

    def get_data(self, video_id):
        video_request = self.youtube.videos().list(
            part="contentDetails,snippet,player",
            id=video_id
        )

        video_response = video_request.execute()

        if "items" in video_response and video_response["items"]:
            item = video_response["items"][0]
            vid_data = {
                "id": item["id"],
                "title": item["snippet"]["title"],
                "title_formatted": title_formatting(item["snippet"]["title"]),
                "description": item["snippet"]["description"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "iframe": item["player"]["embedHtml"],
                "categoria": item["snippet"]["tags"],
                "fecha": item["snippet"]["publishedAt"],
                "duracion": item["contentDetails"]["duration"],
            }

            return vid_data

        return None

    def get_video(self):
        video_request = self.youtube.videos().list(
            part="contentDetails,snippet,player",
            id=self.vid_id
        )

        video_response = video_request.execute()

        item = video_response["items"][0]
        vid_data = {
            "id": item["id"],
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "iframe": item["player"]["embedHtml"],
            "categoria": item["snippet"]["tags"],
            "fecha": item["snippet"]["publishedAt"],
            "duracion": item["contentDetails"]["duration"],
        }

        return vid_data
    
    