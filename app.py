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
CORS(app) 

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/extract_features', methods=['POST'])
def extract_features():
    try:
        data = request.json
        img_data = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(img_data))
        
        features = extractor.extract(img)
        return jsonify({'features': features.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query_features = np.array(data['features'])
        metric = data['metric'] # Default to 'cosine' if not provided
        top_n=int(data['topK'])
        similar_images = search_similar_images(query_features,metric,top_n)
        
        return jsonify(similar_images)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def search_similar_images(query_features, metric,top_n=5):
    # Elasticsearch query using cosine similarity
    #possible metrics : L1 : "1 / (1 + l1norm(params.queryVector, 'my_dense_vector'))"
    #                    Cosine : "cosineSimilarity(params.query_vector, 'image_embedding') + 1.0"
    #                    Euclidien : "1 / (1 + l2norm(params.queryVector, 'my_dense_vector'))"
    print(f"Selected Metric Is{metric}")
    query = {
        "size": top_n,
        "_source": ["image_id", "image_name", "relative_path"],
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": f"{metric}",
                    "params": {"query_vector": query_features.tolist()}
                }
            }
        }
    }

    response = es.search(index='my-image-embeddings', body=query)
    
    return [{
        'image_id': hit['_source']['image_id'],
        'image_name': hit['_source']['image_name'],
        'relative_path': hit['_source']['relative_path']
    } for hit in response['hits']['hits']]

if __name__ == '__main__':
    app.run(debug=True)
