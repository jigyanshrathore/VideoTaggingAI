import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from frameprocess import extract_frames, analyze_frames_with_vision, generate_story

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"yourpathofapikey.json"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './video_data'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

label_frames = {}


@app.route('/')
def index():
    """Root route to display the upload page."""
    return render_template("upload.html")


@app.route('/upload', methods=['POST'])
def upload_video():
    """
    Flask route for uploading and analyzing a video.

    Returns:
        Response: JSON containing video analysis and story summary.
    """
    global label_frames 

    if 'video' not in request.files:
        return jsonify({"message": "No video file provided"}), 400

    video = request.files['video']
    if video.filename == '':
        return jsonify({"message": "No selected video"}), 400

    filename = secure_filename(video.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(video_path)

    try:
        # Step 1: Extract frames
        frames_folder = './video_frames'
        extracted_frames = extract_frames(video_path, frames_folder)

        # Step 2: Analyze frames using Google Vision API
        frame_labels, label_frames = analyze_frames_with_vision(extracted_frames)

        # Step 3: Generate a story from the analysis results
        story = generate_story(frame_labels)

        return jsonify({
            "message": "Video uploaded and analyzed successfully",
            "path": video_path,
            "story": story,
            "analysis": frame_labels
        })

    except Exception as e:
        return jsonify({"message": "Error processing video", "error": str(e)}), 500


@app.route('/search', methods=['GET'])
def search_frames():
    """
    Searches for frames containing the given keyword.

    Query Params:
        - keyword (str): The keyword to search for.

    Returns:
        Response: JSON containing the list of frames where the keyword appears.
    """
    global label_frames  

    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"message": "No keyword provided"}), 400

    try:
        if keyword in label_frames:
            return jsonify({
                "message": f"Frames containing '{keyword}'",
                "frames": label_frames[keyword]
            })
        else:
            return jsonify({
                "message": f"No frames found for keyword '{keyword}'"
            })

    except Exception as e:
        return jsonify({"message": "Error searching frames", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
