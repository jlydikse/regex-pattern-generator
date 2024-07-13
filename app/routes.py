from flask import render_template, request, redirect, url_for
from app import app
from app.ocr import perform_ocr
from app.regex_generator import generate_regex_patterns, cluster_texts, generate_patterns_from_clusters
from app.error_detection import * 
from app.correction_suggestion import *
import os

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            ocr_text = perform_ocr(file_path)
            regex_patterns = generate_regex_patterns(ocr_text)

            texts = [ocr_text, "example text one", "example text two", "different example"]
            model, vectorizer = cluster_texts(texts)
            clustered_patterns = generate_patterns_from_clusters(model, vectorizer, texts)

            return render_template('index.html', ocr_text=ocr_text, regex_patterns=regex_patterns, clustered_patterns=clustered_patterns)
    return render_template('index.html')
