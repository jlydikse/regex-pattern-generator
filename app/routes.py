from flask import render_template, request, redirect, url_for, jsonify, session
from app import app
from app.ocr import perform_ocr
from app.regex_generator import generate_regex_patterns, cluster_texts, generate_patterns_from_clusters
from app.error_correction import detect_and_correct_errors
from app.correction_suggestion import *
import os

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.secret_key = 'your_secret_key'  # Needed to use sessions

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

            # Store the file name in the session
            session['uploaded_file_name'] = file.filename

            # Detect and correct errors
            error_suggestions, corrected_text = detect_and_correct_errors(ocr_text)
            session['error_suggestions'] = error_suggestions  # Store suggestions in session
            session['corrected_text'] = corrected_text  # Store corrected text in session

            return render_template('index.html', ocr_text=ocr_text, regex_patterns=regex_patterns, clustered_patterns=clustered_patterns, error_suggestions=error_suggestions)
    return render_template('index.html')

@app.route('/save_suggestion', methods=['POST'])
def save_suggestion():
    data = request.json
    image = session.get('uploaded_file_name', 'Unknown')  # Retrieve the file name from the session
    regex = data.get('regex')
    status = data.get('status')

    # Define the file path
    file_path = "C:/Users/jlydi/OneDrive/Desktop/BYU-Idaho/CSE 499 Senior Project/RegexGeneratorProject/regex-pattern-generator/app/static/approvedRegexPatterns.txt"
    
    # Write the suggestion to the file
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"Image= {image} Regex= {regex}, Status= {status}\n")

    # Implement your logic to save the suggestion
    print(f'Suggestion saved: Image={image}, Regex={regex}, Status={status}')

    return jsonify(success=True)

@app.route('/save_correction', methods=['POST'])
def save_correction():
    data = request.json
    status = data.get('status')
    corrected_text = session.get('corrected_text', 'Unknown')
    image = session.get('uploaded_file_name', 'Unknown')  # Retrieve the file name from the session



    # Define the file path
    file_path = "C:/Users/jlydi/OneDrive/Desktop/BYU-Idaho/CSE 499 Senior Project/RegexGeneratorProject/regex-pattern-generator/app/static/correctedTexts.txt"

    # Write the correction to the file
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"Image= {image}, Corrected Text= {corrected_text}, Status= {status}\n")

    print(f'Correction saved: Image={image}, Corrected Text={corrected_text}, Status={status}')

    return jsonify(success=True)
