import os
import cv2
from google.cloud import vision


def extract_frames(video_path, output_folder, frame_interval=30):
   
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f"Error: Cannot open video file {video_path}")
    
    os.makedirs(output_folder, exist_ok=True)
    frame_count = 0
    success, frame = cap.read()

    while success:
        if frame_count % frame_interval == 0:  
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
        success, frame = cap.read()
        frame_count += 1

    cap.release()
    return output_folder


def analyze_frames_with_vision(frames_folder):
  
    vision_client = vision.ImageAnnotatorClient()
    frame_labels = {}
    label_frames = {}

    for frame_file in os.listdir(frames_folder):
        if frame_file.endswith('.jpg'):
            frame_path = os.path.join(frames_folder, frame_file)

            with open(frame_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = vision_client.label_detection(image=image)

            if response.error.message:
                raise Exception(f"Google Vision API error: {response.error.message}")

            labels = [label.description for label in response.label_annotations]
            frame_labels[frame_file] = labels

            for label in labels:
                if label not in label_frames:
                    label_frames[label] = []
                label_frames[label].append(frame_file)

    return frame_labels, label_frames



def generate_story(analysis_results):
   
    label_count = {}

    for labels in analysis_results.values():
        for label in labels:
            label_count[label] = label_count.get(label, 0) + 1

    sorted_labels = sorted(label_count.items(), key=lambda x: x[1], reverse=True)

    story = "This video predominantly features: "
    story += ", ".join([f"{label} ({count} times)" for label, count in sorted_labels[:5]])
    return story
