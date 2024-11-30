import os
from google.cloud import vision
from google.cloud import speech
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/HP/Desktop/aivideotagging/majestic-cairn-442720-q2-1a0c8e4b7aba.json"

vision_client = vision.ImageAnnotatorClient()

speech_client = speech.SpeechClient()

storage_client = storage.Client()

print("Google Cloud services authenticated successfully!")
