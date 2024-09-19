document.addEventListener('DOMContentLoaded', function() {
    const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
        mode: 'python',
        theme: 'default',
        lineNumbers: true,
        autofocus: true
    });

    const runCodeButton = document.getElementById('run-code');
    const submitSolutionButton = document.getElementById('submit-solution');
    const codeOutput = document.getElementById('code-output');
    const aiFeedback = document.getElementById('ai-feedback');

    runCodeButton.addEventListener('click', function() {
        const code = editor.getValue();
        // In a real application, you would send this code to a backend for execution
        // For now, we'll just display the code in the output area
        codeOutput.textContent = "Code output (not executed):\n\n" + code;
    });

    submitSolutionButton.addEventListener('click', function() {
        const code = editor.getValue();
        fetch('/submit_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code }),
        })
        .then(response => response.json())
        .then(data => {
            aiFeedback.textContent = data.feedback;
        })
        .catch((error) => {
            console.error('Error:', error);
            aiFeedback.textContent = 'An error occurred while submitting your code. Please try again.';
        });
    });
});