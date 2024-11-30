import os
from google.cloud import vision
from google.cloud import speech
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "apipath.json"

vision_client = vision.ImageAnnotatorClient()

speech_client = speech.SpeechClient()

storage_client = storage.Client()

print("Google Cloud services authenticated successfully!")
