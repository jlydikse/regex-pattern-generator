document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const inputText = document.getElementById('inputText');
    const generatedPattern = document.getElementById('generatedPattern');
    const testBtn = document.getElementById('testBtn');
    const testInput = document.getElementById('testInput');
    const testResults = document.getElementById('testResults');
    const acceptBtn = document.getElementById('acceptBtn');
    const denyBtn = document.getElementById('denyBtn');
    const editPatternBtn = document.getElementById('editPatternBtn');
    const patternTextarea = document.getElementById('patternTextarea');
    const suggestedPatternElement = document.getElementById('suggestedPattern');
    const selectedPatternInput = document.getElementById('selected_regex_pattern');
    const uploadedFileNameInput = document.getElementById('uploadedFileName');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');

    // Set the uploaded file name in the hidden input field
    fileInput.addEventListener('change', function() {
        const fileName = fileInput.files[0].name;
        uploadedFileNameInput.value = fileName;
    });

    generateBtn.addEventListener('click', function() {
        const text = inputText.value;
        if (text) {
            generatedPattern.textContent = `Generated pattern for: ${text}`;
        }
    });

    testBtn.addEventListener('click', function() {
        const testText = testInput.value;
        const patternText = generatedPattern.textContent;
        if (testText && patternText) {
            testResults.textContent = `Tested "${testText}" against pattern: ${patternText}`;
        }
    });

    function findLongestPreTag() {
        const patterns = document.querySelectorAll('#advancedPatterns .pattern');
        let longestPreTag = '';
        let associatedRegex = '';

        patterns.forEach(pattern => {
            const preTag = pattern.querySelector('pre');
            const regexPattern = pattern.querySelector('h4').textContent;

            if (preTag.textContent.length > longestPreTag.length) {
                longestPreTag = preTag.textContent;
                associatedRegex = regexPattern;
            }
        });

        return associatedRegex;
    }

    const selectedPattern = findLongestPreTag();
    suggestedPatternElement.textContent = selectedPattern;
    selectedPatternInput.value = selectedPattern;

    acceptBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default form submission
        alert('Suggestion accepted: ' + selectedPattern);
        saveSuggestion('accepted');
    });

    denyBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default form submission
        alert('Suggestion denied: ' + selectedPattern);
        saveSuggestion('denied');
    });

    function saveSuggestion(status) {
        const imageName = uploadedFileNameInput.value;
        const suggestion = selectedPattern;

        const suggestionData = {
            image: imageName,
            regex: suggestion,
            status: status
        };

        fetch('/save_suggestion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(suggestionData)
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            console.log('Suggestion saved:', data);
        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }

    editPatternBtn.addEventListener('click', function() {
        const newPattern = patternTextarea.value;
        generatedPattern.textContent = newPattern;
    });
});
