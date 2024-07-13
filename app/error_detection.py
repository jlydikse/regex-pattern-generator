def check_for_errors(text):
    errors = []
    if not text:
        errors.append('No text found.')
    if len(text) < 5:
        errors.append('Text is too short.')
    return errors

def suggest_corrections(errors):
    suggestions = {}
    for error in errors:
        if error == 'No text found.':
            suggestions[error] = 'Ensure the uploaded image contains text.'
        if error == 'Text is too short.':
            suggestions[error] = 'Provide a longer text sample.'
    return suggestions