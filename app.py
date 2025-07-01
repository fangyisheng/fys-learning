import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# We will import other necessary modules later
from werkzeug.utils import secure_filename
import google.generativeai as genai
import PyPDF2 # Or other PDF library

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Configuration for file uploads and Gemini API
UPLOAD_FOLDER = 'uploads'
KNOWLEDGE_BASE_FOLDER = 'knowledge_base'
ALLOWED_EXTENSIONS = {'pdf'}

# It's better to set this as an environment variable
# For this exercise, we'll use the one provided, but warn about security.
# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_API_KEY = "AIzaSyB9H4l4XDdlL81jiEzK9dvMlnnD2uyO_GM" # User provided

if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY is not set. Please provide it or set the environment variable.")
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("Gemini API configured successfully.")
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['KNOWLEDGE_BASE_FOLDER'] = KNOWLEDGE_BASE_FOLDER

# Ensure the upload and knowledge base directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or "" # Add empty string if None
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return None
    return text

@app.route('/')
def index():
    session.clear() # Clear session on new visit
    # Initialize session variables if they don't exist
    session.setdefault('chat_history', [])
    session.setdefault('pdf_processed', False)
    session.setdefault('pdf_filename', None)
    session.setdefault('pdf_text', None)
    # Initialize the generative model (safer to do it once if settings are fixed)
    # Or, initialize it within the chat route if model settings might change
    try:
        model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text-only for now
        session['gemini_initialized'] = True
    except Exception as e:
        print(f"Error initializing Gemini model in index: {e}")
        session['gemini_initialized'] = False

    return render_template('index.html',
                           chat_history=session['chat_history'],
                           pdf_processed=session['pdf_processed'],
                           pdf_filename=session['pdf_filename'],
                           knowledge_bases=get_knowledge_bases(),
                           gemini_initialized=session.get('gemini_initialized', False))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the PDF
        pdf_text = extract_text_from_pdf(filepath)
        if pdf_text is not None:
            session['pdf_processed'] = True
            session['pdf_filename'] = filename
            session['pdf_text'] = pdf_text
            session['chat_history'] = [] # Reset chat history for new PDF
            # For now, just store text. Image extraction will be more complex.
            print(f"Extracted text from {filename}: {len(pdf_text)} characters")
        else:
            session['pdf_processed'] = False
            session['pdf_filename'] = filename # Show filename even if processing failed
            session['pdf_text'] = None
            # Optionally, add a message to the user about processing failure
            print(f"Failed to extract text from {filename}")

        return redirect(url_for('index'))
    return redirect(request.url)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    if not session.get('pdf_processed') or not session.get('pdf_text'):
        return jsonify({'error': 'PDF not processed or no text found. Please upload a PDF first.'}), 400

    if not session.get('gemini_initialized'):
        return jsonify({'error': 'Gemini API not initialized. Check API key and server logs.'}), 500

    pdf_text_summary = (session['pdf_text'][:1000] + '...') if len(session['pdf_text']) > 1000 else session['pdf_text']
    prompt = f"You are a helpful assistant. A user has uploaded a PDF with the following content (summary/beginning shown): '{pdf_text_summary}'. Now the user asks: '{user_message}'. Based on the FULL PDF text (which you should imagine you have access to, even though I only showed a summary here for context), answer the user's question. If the question is not related to the PDF, try to answer it generally but state that it's not from the PDF. If the question seems to ask for information beyond the PDF's content, clarify that."

    try:
        # For gemini-pro (text only)
        model = genai.GenerativeModel('gemini-pro') # Re-initialize or ensure it's available

        # Construct chat history for the model
        # The google-generativeai library's `start_chat` method handles history internally.
        # We need to adapt our session['chat_history'] to its format if we want to use it directly.
        # For now, let's manage a simple version of history for the prompt, or use start_chat.

        # Option 1: Simple prompt including current question and PDF context
        # response = model.generate_content(prompt)

        # Option 2: Using start_chat for more conversational context
        # The chat history needs to be in the format: [{'role': 'user'/'model', 'parts': [text]}]
        formatted_history = []
        for entry in session.get('chat_history', []):
            role = 'user' if entry['role'] == 'user' else 'model'
            formatted_history.append({'role': role, 'parts': [entry['text']]})

        # Add the current PDF context as a strong system-like message if not too long
        # This is a simplified way to give context. For very long PDFs, summarization or RAG is needed.
        # For now, we are assuming the model can handle the context given with the prompt.
        # The `pdf_text_summary` is already in the `prompt`.

        chat_session = model.start_chat(history=formatted_history)
        response = chat_session.send_message(user_message) # Send only the user's current message

        bot_reply = response.text

        # Update our session chat history
        session['chat_history'].append({'role': 'user', 'text': user_message})
        session['chat_history'].append({'role': 'bot', 'text': bot_reply})
        session.modified = True # Ensure session is saved

        return jsonify({'reply': bot_reply})

    except Exception as e:
        print(f"Error communicating with Gemini API: {e}")
        # Check for specific API errors if possible, e.g., response.prompt_feedback
        # if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
        #     print(f"Prompt feedback: {response.prompt_feedback}")
        # if response.candidates[0].finish_reason != 1 : # 1 = STOP
        #     print(f"Finish reason: {response.candidates[0].finish_reason}")
        #     print(f"Safety Ratings: {response.candidates[0].safety_ratings}")


        return jsonify({'error': f'Failed to get response from Gemini: {str(e)}'}), 500

@app.route('/save_kb', methods=['POST'])
def save_knowledge_base():
    if not session.get('pdf_processed') or not session.get('pdf_filename') or not session.get('pdf_text'):
        return jsonify({'error': 'No PDF processed to save as knowledge base.', 'success': False}), 400

    kb_filename = session['pdf_filename'] + ".json" # Simple naming, might need sanitization or uniqueness checks
    kb_filepath = os.path.join(app.config['KNOWLEDGE_BASE_FOLDER'], secure_filename(kb_filename))

    # For now, the "knowledge base" will just store the extracted text and original filename.
    # More advanced KBs would involve embeddings, indexing, etc.
    kb_data = {
        'original_filename': session['pdf_filename'],
        'text_content': session['pdf_text'],
        'created_at': datetime.now(timezone.utc).isoformat() # Updated to use timezone.utc
    }

    try:
        with open(kb_filepath, 'w') as f:
            json.dump(kb_data, f, indent=4)
        # Update the list of KBs for the frontend
        session['knowledge_bases'] = get_knowledge_bases()
        return jsonify({'message': f"Knowledge base '{kb_filename}' saved successfully!", 'success': True, 'kb_name': kb_filename})
    except Exception as e:
        print(f"Error saving knowledge base {kb_filename}: {e}")
        return jsonify({'error': f'Failed to save knowledge base: {str(e)}', 'success': False}), 500

@app.route('/load_kb', methods=['POST'])
def load_knowledge_base_route():
    data = request.get_json()
    kb_name = data.get('kb_name')

    if not kb_name:
        return jsonify({'error': 'No knowledge base name provided.', 'success': False}), 400

    kb_filepath = os.path.join(app.config['KNOWLEDGE_BASE_FOLDER'], secure_filename(kb_name))

    if not os.path.exists(kb_filepath):
        return jsonify({'error': f"Knowledge base '{kb_name}' not found.", 'success': False}), 404

    try:
        with open(kb_filepath, 'r') as f:
            kb_data = json.load(f)

        # Load this KB's data into the session as if a PDF was just uploaded
        session['pdf_processed'] = True
        session['pdf_filename'] = kb_data.get('original_filename', kb_name.replace(".json", ""))
        session['pdf_text'] = kb_data.get('text_content', "")
        session['chat_history'] = [] # Reset chat history for the loaded KB
        # session['current_kb_name'] = kb_name # Optional: track loaded KB

        print(f"Knowledge base {kb_name} loaded into session.")
        return jsonify({
            'message': f"Knowledge base '{kb_name}' loaded successfully!",
            'success': True,
            'pdf_filename': session['pdf_filename'],
            'pdf_processed': True
        })
    except Exception as e:
        print(f"Error loading knowledge base {kb_name}: {e}")
        return jsonify({'error': f'Failed to load knowledge base: {str(e)}', 'success': False}), 500


def get_knowledge_bases():
    kb_folder = app.config['KNOWLEDGE_BASE_FOLDER']
    if not os.path.exists(kb_folder):
        os.makedirs(kb_folder, exist_ok=True) # Ensure it exists
        return []
    return sorted([f for f in os.listdir(kb_folder) if f.endswith('.json') and os.path.isfile(os.path.join(kb_folder, f))])


# We will add more routes and functions later
import json
from datetime import datetime, timezone

if __name__ == '__main__':
    if GOOGLE_API_KEY == "AIzaSyB9H4l4XDdlL81jiEzK9dvMlnnD2uyO_GM":
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("WARNING: You are using a hardcoded API key in the script.")
        print("This is insecure and should not be done in production.")
        print("Consider using environment variables for API keys.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    elif not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set and no hardcoded key found.")
        print("Please set it by running 'export GOOGLE_API_KEY=\"your_api_key_here\"' in your terminal before starting the app,")
        print("or provide it if the script prompts for it.")
        # exit(1) # Optionally exit if no key is available
    else:
        print(f"Google API Key found (from env var): {GOOGLE_API_KEY[:5]}...{GOOGLE_API_KEY[-5:]}")

    app.run(debug=True)
