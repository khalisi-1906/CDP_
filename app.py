from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import nltk
import re

nltk.download('punkt')
app = Flask(__name__)
CORS(app)

# Data Ingestion and Preprocessing functions (same as before, omitted for brevity)
def scrape_docs(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = ' '.join(p.text for p in soup.find_all('p'))
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def preprocess_text(text):
    if text:
        text = text.lower()
        text = ' '.join(text.split())
    return text

def chunk_text(text, chunk_size=500):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_len = 0

    for sentence in sentences:
        sentence_len = len(sentence.split())
        if current_len + sentence_len > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_len = sentence_len
        else:
            current_chunk.append(sentence)
            current_len += sentence_len
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

docs_urls = {
    'segment': [
        'https://segment.com/docs/connections/sources/',
        'https://segment.com/docs/connections/destinations/',
        'https://segment.com/docs/protocols/tracking-api/'
    ],
    'mparticle': [
        'https://docs.mparticle.com/developers/data-planning/create-an-event',
        'https://docs.mparticle.com/guides/audience-builder',
        'https://docs.mparticle.com/integrations/google-analytics'
    ],
    'lytics': [
        'https://docs.lytics.com/docs/user-segments/',
        'https://docs.lytics.com/docs/connectors/',
        'https://docs.lytics.com/docs/data-import/'
    ],
    'zeotap': [
        'https://docs.zeotap.com/data-integration/connectors/',
        'https://docs.zeotap.com/data-management/identity-resolution/',
        'https://docs.zeotap.com/data-activation/audiences/'
    ]
}

documents = []
for cdp, urls in docs_urls.items():
    for url in urls:
        raw_text = scrape_docs(url)
        if raw_text:
            cleaned_text = preprocess_text(raw_text)
            if cleaned_text:
                chunks = chunk_text(cleaned_text)
                for i, chunk in enumerate(chunks):
                    documents.append({'text': chunk, 'url': url, 'cdp': cdp, 'chunk_id': i})

# Text Embedding and Indexing functions (same as before, omitted for brevity)
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode([doc['text'] for doc in documents])
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings).astype('float32'))

# Chatbot Logic functions (same as before, omitted for brevity)
def answer_question(question, threshold=0.3):
    question = preprocess_text(question)
    question_embedding = model.encode(question)
    D, I = index.search(np.array(question_embedding).astype('float32').reshape(1, -1), 5)

    results = []
    for i, distance in zip(I[0], D[0]):
        if distance < threshold:
            results.append(documents[i])
    return results

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        question = data.get('question')

        if not question:
            return jsonify({"message": "No question provided"}), 400  # Return 400 for bad request

        results = answer_question(question)

        if results:
            return jsonify({"answers": results}), 200
        else:
            return jsonify({"message": "I'm unable to answer this question as it is unrelated to CDPs."}), 200
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"message": "An unexpected error occurred."}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)