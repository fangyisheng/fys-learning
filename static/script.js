// Basic frontend JavaScript for interaction (will be expanded)

document.addEventListener('DOMContentLoaded', function() {
    // Placeholder for now, will add more interactivity later
    console.log("Document loaded. Static script.js is active.");

    // Example: Show/hide chat section (this logic will be improved)
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                // For now, just log. Later, this might trigger showing the chat.
                console.log("File selected:", this.files[0].name);
            }
        });
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const messageText = userInput.value.trim();
    const chatHistoryDiv = document.getElementById('chat-history');

    if (messageText === "") {
        return;
    }

    // Display user message
    appendMessageToChatHistory('user', messageText);

    // Clear input
    userInput.value = "";
    chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight; // Scroll to bottom

    // Send message to backend
    fetch('/chat', { // Ensure this route exists in app.py
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: messageText }),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Network response was not ok'); });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            appendMessageToChatHistory('bot', "Error: " + data.error);
        } else {
            appendMessageToChatHistory('bot', data.reply);
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
        appendMessageToChatHistory('bot', "Sorry, an error occurred: " + error.message);
    });
}

function appendMessageToChatHistory(senderRole, text) {
    const chatHistoryDiv = document.getElementById('chat-history');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(senderRole === 'user' ? 'user-message' : 'bot-message');

    const senderSpan = document.createElement('span');
    senderSpan.classList.add('sender');
    senderSpan.textContent = senderRole === 'user' ? 'You: ' : 'Gemini: ';

    const textSpan = document.createElement('span');
    textSpan.classList.add('text');
    textSpan.textContent = text;

    messageDiv.appendChild(senderSpan);
    messageDiv.appendChild(textSpan);
    chatHistoryDiv.appendChild(messageDiv);
    chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight; // Scroll to bottom
}


// Add event listener for Enter key in chat input
const userInputField = document.getElementById('user-input');
if (userInputField) {
    userInputField.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

// Functions for Knowledge Base (to be implemented more fully later)
function saveToKnowledgeBase() {
    // This will be implemented to call a backend endpoint
    console.log("saveToKnowledgeBase called");
    fetch('/save_kb', { method: 'POST' }) // Ensure this route exists
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if(data.success) window.location.reload(); // Refresh to see updated KB list
        })
        .catch(error => {
            console.error("Error saving to KB:", error);
            alert("Error saving to knowledge base.");
        });
}

function loadKnowledgeBase(kbName) {
    // This will be implemented to call a backend endpoint
    console.log("loadKnowledgeBase called with:", kbName);
    fetch('/load_kb', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kb_name: kbName })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        if(data.success) {
            // Update UI to reflect loaded KB, e.g., refresh chat or PDF info
            window.location.reload(); // Simple refresh for now
        }
    })
    .catch(error => {
        console.error("Error loading KB:", error);
        alert("Error loading knowledge base.");
    });
}

// Update UI based on session state (e.g., show/hide chat)
// This is partially handled by Flask templates, but JS can enhance it.
document.addEventListener('DOMContentLoaded', function() {
    const chatSection = document.getElementById('chat-section');
    const knowledgeBaseSection = document.getElementById('knowledge-base-section');
    // The display is now primarily controlled by Jinja templates based on session['pdf_processed']
    // We can add more dynamic JS updates here if needed.

    // If there's an upload status message from a redirect, display it or handle it
    const uploadStatusDiv = document.getElementById('upload-status');
    if (uploadStatusDiv && uploadStatusDiv.textContent.includes("Processed") && chatSection) {
        // chatSection.style.display = 'block'; // Handled by Jinja
        // knowledgeBaseSection.style.display = 'block'; // Handled by Jinja
    }
    console.log("PDF processing status from HTML (via Jinja):", chatSection.style.display);
});
