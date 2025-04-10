"""Flask application for emotion detection web interface."""
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')
client = MongoClient(mongo_uri)
db = client['emotion_detection']
emotions_collection = db['emotions']

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/emotions', methods=['POST'])
def save_emotion():
    """Save emotion data from ML client to MongoDB."""
    data = request.json
    if not data or 'emotion' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    emotion_record = {
        'emotion': data['emotion'],
        'timestamp': datetime.utcnow(),
        'confidence': data.get('confidence', None)
    }
    emotions_collection.insert_one(emotion_record)
    return jsonify({'status': 'success'}), 201

@app.route('/api/emotions/recent', methods=['GET'])
def get_recent_emotions():
    """Get recent emotion records."""
    recent_emotions = list(
        emotions_collection.find(
            {},
            {'_id': 0}
        ).sort('timestamp', -1).limit(10)
    )
    return jsonify(recent_emotions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
