﻿# ElasticSearch_ImageSimiliarities_VGG16featureExtractor_JS_Python
 ## Project Overview

This project demonstrates image similarity search using Elasticsearch and a VGG16-based feature extractor. Images are encoded into vector embeddings, indexed in Elasticsearch, and compared for similarity based on metrics such as cosine similarity or L1 distance. A Flask-based web application with JavaScript provides a user interface for uploading images, viewing results, and modifying parameters like the similarity metric and number of top results.

---

## Video demo: 

To get started quickly, watch this tutorial that walks you through a demo:


https://github.com/user-attachments/assets/750f1d4a-8249-4c1b-954a-2ec4a9f11926

*You will find below a detailed step by step guide:

---
## Goals

1. Encode images into feature vectors using VGG16.
2. Store these embeddings in an Elasticsearch database.
3. Allow users to search for images similar to a given input through a web interface.

---

## Requirements

### Python Environment
- **Python version:** 3.8 (recommended to use `conda`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/08Youssef08/ElasticSearch_ImageSimiliarities_VGG16featureExtractor_JS_Python.git
   cd ElasticSearch_ImageSimiliarities_VGG16featureExtractor_JS_Python
   ```
2. Set up a virtual environment:
   ```bash
   conda create -n searchenv python=3.8
   conda activate searchenv
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download and install Elasticsearch:
   - Ensure you have [Elasticsearch](https://www.elastic.co/downloads/elasticsearch) installed. Extract the downloaded file and locate the `bin` folder.

---

## Steps to Run the Project

### 1. Start Elasticsearch
- Navigate to the `bin` directory of your Elasticsearch installation.
- For Windows, execute:
  ```bash
  elasticsearch.bat
  ```
- Wait until Elasticsearch starts on port `9200`.

### 2. Index Images
- Ensure your images are placed in the folder: `static/images`.
- Run the image indexing script:
   ```bash
   python create_image_embeddings.py
   ```
- This script:
  1. Encodes images in `static/images` into embeddings using VGG16.
  2. Stores the embeddings, image IDs, and metadata in Elasticsearch.

### 3. Run the Flask App
- Start the application server:
   ```bash
   python app.py
   ```
- Open the app in your browser at: `http://127.0.0.1:5000`.

### 4. Search for Similar Images
- Upload or drag and drop an image into the application.
- The app processes the input image, converts it to a feature vector, and queries Elasticsearch for the most similar images.
- Adjust parameters like:
  - **Similarity metric** (e.g., cosine similarity, L1).
  - **Top-k results** (e.g., top 5, top 10).

---

## Key Notes

1. **Dataset:** You can use any dataset; by default, the example contains animal images from Kaggle.
2. **Memory:** Ensure sufficient memory for Elasticsearch during image indexing.
3. **Custom Metrics:** Modify metrics directly in the code or use the app interface for adjustments.
4. **Elasticsearch Port:** Elasticsearch runs on port `9200`. The Flask app connects to this port.

---

## File Structure

- `static/`: Contains the images for indexing.
- `templates/`: Holds HTML templates for the Flask app.
- `app.py`: Main Flask application.
- `create_image_embeddings.py`: Script to generate and index image embeddings.
- `feature_extractor.py`: Implements VGG16-based feature extraction.

---

## Troubleshooting

- **Memory Issues:** If you encounter warnings about insufficient memory during indexing, increase your system's available memory or reduce the dataset size.
- **Image Format Errors:** Ensure uploaded images are in a supported format (e.g., `.jpg`, `.png`).
- **Elasticsearch Status:** Confirm Elasticsearch is running and accessible on port `9200`.

---
