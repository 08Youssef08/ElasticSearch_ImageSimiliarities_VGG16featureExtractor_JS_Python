from feature_extractor import FeatureExtractor
from elasticsearch import Elasticsearch
from PIL import Image
import os


def create_image_embeddings(es_host):
    es = Elasticsearch(
        ES_HOST,
        request_timeout=ES_TIMEOUT,
    )
    
    index_name = 'my-image-embeddings'
    
    # Ensure the index exists
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
    
    # Set up your feature extractor
    feature_extractor = FeatureExtractor()  # Initialize your extractor

    images_directory = './static/images'
    for root, dirs, files in os.walk(images_directory):
        for file in files:
            if file.endswith(('jpeg', 'jpg', 'png')):
                image_path = os.path.join(root, file)
                image_id = os.path.splitext(file)[0]
                
                try:
                    # Generate embeddings
                    img = Image.open(image_path)  # Open the image file
                    embedding = feature_extractor.extract(img)
                    print(embedding)
                    
                    # Create document
                    doc = {
                        "image_id": image_id,
                        "image_name": file,
                        "image_embedding": embedding.tolist(),  # Convert numpy array to list
                        "relative_path": os.path.relpath(image_path, images_directory)
                    }
                    print(doc)
                    
                    # Save document to Elasticsearch
                    es.index(index=index_name, document=doc)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == '__main__':
    ES_HOST = "http://127.0.0.1:9200/"
    ES_USER = "elastic"
    ES_PASSWORD = "changeme"
    ES_TIMEOUT = 360000

    DEST_INDEX = "my-image-embeddings"
    DELETE_EXISTING = True
    CHUNK_SIZE = 100

    PATH_TO_IMAGES = "../app/static/images/**/*.jp*g"
    PREFIX = "../app/static/images/"
    try:
        create_image_embeddings(ES_HOST)
    except Exception as e:
        print(f"An error occurred while creating image embeddings: {e}")
