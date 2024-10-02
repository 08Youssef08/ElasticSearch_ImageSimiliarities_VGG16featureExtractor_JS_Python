from flask import Flask, request, jsonify, render_template
from feature_extractor import FeatureExtractor
from flask_cors import CORS
from elasticsearch import Elasticsearch
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)
extractor = FeatureExtractor()
CORS(app)  # Enable CORS

# Set up Elasticsearch connection
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

@app.route('/extract_features', methods=['POST'])
def extract_features():
    try:
        data = request.json
        img_data = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(img_data))
        
        # Extract features using the FeatureExtractor
        features = extractor.extract(img)
        return jsonify({'features': features.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/search', methods=['POST'])
def search():
    try:
        # Get the features from the request (sent by JavaScript)
        data = request.get_json()
        query_features = np.array(data['features'])
        
        # Search for similar images using the query features
        similar_images = search_similar_images(query_features)
        
        return jsonify(similar_images)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def search_similar_images(query_features, top_n=5):
    # Elasticsearch query using cosine similarity
    query = {
        "size": top_n,
        "_source": ["image_id", "image_name", "relative_path"],
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'image_embedding') + 1.0",
                    "params": {"query_vector": query_features.tolist()}
                }
            }
        }
    }

    # Perform the search in the 'my-image-embeddings' index
    response = es.search(index='my-image-embeddings', body=query)
    
    # Extract and return the image IDs and their relative paths
    return [{
        'image_id': hit['_source']['image_id'],
        'image_name': hit['_source']['image_name'],
        'relative_path': hit['_source']['relative_path']
    } for hit in response['hits']['hits']]

if __name__ == '__main__':
    app.run(debug=True)
