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

    acceptBtn.addEventListener('click', function() {
        alert('Suggestion accepted');
    });

    denyBtn.addEventListener('click', function() {
        alert('Suggestion denied');
    });

    editPatternBtn.addEventListener('click', function() {
        const newPattern = patternTextarea.value;
        generatedPattern.textContent = newPattern;
    });
});
