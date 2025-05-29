from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

def upload_video(video_path, title, description, thumbnail_path):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as f:
            creds = pickle.load(f)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes)
        creds = flow.run_local_server()
        with open("token.pickle", "wb") as f:
            pickle.dump(creds, f)

    youtube = build("youtube", "v3", credentials=creds)
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["daily trend", "news", "AI", "automation"],
            "categoryId": "25"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    video = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=video_path
    ).execute()

    youtube.thumbnails().set(
        videoId=video["id"],
        media_body=thumbnail_path
    ).execute()
