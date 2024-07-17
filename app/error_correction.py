import re

# Define the common OCR errors and their corrections
ERROR_CORRECTIONS = {
    r'\+\#': '∞',
    r'\\soo\\s': '∞',
    r'\*\#': '*',
    r'(?<=\b[A-Za-z])0(?=[A-Za-z]\b)': 'o',  # 0 surrounded by letters should be 'o'
    r'\= @': '∞',
    # Add more patterns and corrections as needed
}

def detect_and_correct_errors(text):
    suggestions = []
    corrected_text = text
    for error_pattern, correction in ERROR_CORRECTIONS.items():
        matches = re.findall(error_pattern, text)
        if matches:
            suggestions.append((matches, error_pattern, correction))
            corrected_text = re.sub(error_pattern, correction, corrected_text)
    return suggestions, corrected_text
