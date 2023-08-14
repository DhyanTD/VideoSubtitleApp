from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
SUBTITLES_FOLDER = 'subtitles'
THUMBNAIL_FOLDER = 'thumbnails'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SUBTITLES_FOLDER'] = SUBTITLES_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER

# @app.route('/')
# def index():
#     return render_template('index.html')
if not os.path.exists(app.config['SUBTITLES_FOLDER']):
    os.makedirs(app.config['SUBTITLES_FOLDER'])

if not os.path.exists(app.config['THUMBNAIL_FOLDER']):
    os.makedirs(app.config['THUMBNAIL_FOLDER'])

current_video_id = 0 

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_video_id

    if 'file' not in request.files or 'thumbnail' not in request.files:
        return {'error': 'Missing file part(s)'}

    video_file = request.files['file']
    thumbnail_file = request.files['thumbnail']

    if video_file and thumbnail_file:
        video_extension = os.path.splitext(video_file.filename)[1]
        thumbnail_extension = os.path.splitext(thumbnail_file.filename)[1]

        if video_extension != '.mp4' or thumbnail_extension != '.jpg':
            return {'error': 'Invalid file format'}

        combined_filename = f'{current_video_id+1}{video_extension}'

        video_path = os.path.join(app.config['UPLOAD_FOLDER'], combined_filename)
        thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], combined_filename.replace('.mp4', '.jpg'))

        video_file.save(video_path)
        thumbnail_file.save(thumbnail_path)

        current_video_id += 1

        return {'message': 'Files uploaded successfully'}

@app.route('/videos/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/subtitles/<filename>')
def get_subtitle_file(filename):
    return send_from_directory(app.config['SUBTITLES_FOLDER'], filename)

@app.route('/thumbnails/<filename>')
def get_thumbnail_file(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

@app.route('/get_uploaded_videos')
def get_uploaded_videos():
    videos = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith(".mp4"):
            video_name = filename.split('.')[0]
            videos.append({
                'name': filename,
                'thumbnail': f'{video_name}.jpg' if os.path.exists(os.path.join(app.config['THUMBNAIL_FOLDER'], f'{video_name}.jpg')) else None
            })
    return {'videos': videos}

@app.route('/add_subtitle', methods=['POST'])
def add_subtitle():
    video_name = request.json.get('videoName')
    text = request.json.get('text')
    start_time = request.json.get('startTime')
    end_time = request.json.get('endTime')

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
    subtitle_filename = f'{current_video_id+1}.vtt'
    subtitle_path = os.path.join(app.config['SUBTITLES_FOLDER'], subtitle_filename)

    if os.path.exists(subtitle_path):
        mode = 'a'
    else:
        mode = 'w'

    with open(subtitle_path, mode) as subtitle_file:
        if mode == 'w':
            subtitle_file.write("WEBVTT\n")
        subtitle_file.write(f"{start_time} --> {end_time}\n")
        subtitle_file.write(f"{text}\n")

    return {'message': 'Subtitle added successfully'}

@app.route('/get_subtitles/<video_name>')
def get_subtitles(video_name):
    subtitles = []
    subtitle_data = ""
    reading_subtitles = False
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
    video_name = os.path.splitext(video_name)[0]
    for filename in os.listdir(app.config['SUBTITLES_FOLDER']):
        if filename.startswith(f"{video_name}") and filename.endswith(".vtt"):
            subtitle_path = os.path.join(app.config['SUBTITLES_FOLDER'], filename)
            with open(subtitle_path, 'r') as subtitle_file:
                for line in subtitle_file:
                    if " --> " in line:
                        reading_subtitles = True
                        subtitle_data += line
                    elif reading_subtitles:
                        text = line.strip()
                        if text:
                            start_time = subtitle_data.split(" --> ")[0]
                            end_time = subtitle_data.split(" --> ")[1].split(" ")[0]
                            subtitles.append({'startTime': start_time, 'endTime': end_time, 'text': text})
                        reading_subtitles = False
                        subtitle_data = ""
    return {'subtitles': subtitles}
    
if __name__ == '__main__':
    app.run(debug=True)
