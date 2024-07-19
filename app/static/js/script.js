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
    const acceptCorrectionBtn = document.getElementById('acceptCorrectionBtn');
    const denyCorrectionBtn = document.getElementById('denyCorrectionBtn');
    const tool1Btn = document.getElementById('tool1Btn');
    const tool2Btn = document.getElementById('tool2Btn');
    const tool3Btn = document.getElementById('tool3Btn');
    const submitPatternBtn = document.getElementById('submitPatternBtn');

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
        event.preventDefault();
        alert('Suggestion accepted: ' + selectedPattern);
        saveSuggestion('accepted');
    });

    denyBtn.addEventListener('click', function(event) {
        event.preventDefault();
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

    submitPatternBtn.addEventListener('click', function(event) {
        event.preventDefault();
        const newPattern = patternTextarea.value.trim();
        if (newPattern) {
            alert('New regex pattern submitted: ' + newPattern);
            submitNewPattern(newPattern);
        } else {
            alert('Please enter a valid regex pattern.');
        }
    });

    function submitNewPattern(pattern) {
        const imageName = uploadedFileNameInput.value.trim();

        const patternData = {
            image: imageName,
            regex: pattern,
            status: 'submitted'  // Assuming 'submitted' is the status we want to save
        };

        fetch('/submit_pattern', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(patternData)
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            console.log('Pattern submitted:', data);
        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }

    acceptCorrectionBtn.addEventListener('click', function(event) {
        event.preventDefault();
        alert('Correction accepted');
        saveCorrection('accepted');
    });

    denyCorrectionBtn.addEventListener('click', function(event) {
        event.preventDefault();
        alert('Correction denied');
        saveCorrection('denied');
    });

    function saveCorrection(status) {
        const correctedText = document.querySelector('#correctionSuggestions pre').textContent;
        const imageName = uploadedFileNameInput.value;

        const correctionData = {
            status: status,
            corrected_text: correctedText,
            image: imageName
        };

        fetch('/save_correction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(correctionData)
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            console.log('Correction saved:', data);
        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }

    tool1Btn.addEventListener('click', function() {
        updatePatternWithThreshold(10);
    });

    tool2Btn.addEventListener('click', function() {
        updatePatternWithThreshold(50);
    });

    tool3Btn.addEventListener('click', function() {
        updatePatternWithThreshold(90);
    });

    function updatePatternWithThreshold(threshold) {
        const ocrText = document.querySelector('pre').textContent;

        fetch('/update_pattern_with_threshold', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ocr_text: ocrText, threshold: threshold })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            if (data.status === 'success') {
                generatedPattern.textContent = `Generated Family Number Pattern: ${data.pattern}`;
            } else {
                alert('Error updating pattern: ' + data.message);
            }
        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
});
