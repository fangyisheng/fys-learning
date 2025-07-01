# Gemini PDF Parser and Chat

This is a simple web application that allows users to upload PDF files, extracts their text content, and provides a chat interface to discuss the PDF's content using Google's Gemini API. Users can also save the extracted text from PDFs as a simple knowledge base for later use.

## Features

-   **PDF Upload:** Upload PDF files through a web interface.
-   **Text Extraction:** Extracts text content from uploaded PDFs (currently using PyPDF2).
-   **Gemini API Integration:** Chat with the Gemini API (gemini-pro model) about the content of the processed PDF.
-   **Chat History:** Maintains chat history for the current session with a PDF.
-   **Knowledge Base:**
    -   Save extracted PDF text as a JSON-based knowledge base file.
    -   Load existing knowledge base files to interact with their content.

## Project Structure

```
.
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── static/               # Static files (CSS, JavaScript)
│   ├── script.js
│   └── style.css
├── templates/            # HTML templates
│   └── index.html
├── uploads/              # Directory for storing uploaded PDFs (created automatically)
├── knowledge_base/       # Directory for storing saved knowledge bases (created automatically)
├── tests/                # Unit tests
│   ├── __init__.py
│   └── test_app.py
└── README.md             # This file
```

## Setup and Running

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Google API Key:**
    The application requires a Google API key for the Gemini API.
    **IMPORTANT SECURITY NOTE:** The application currently uses a hardcoded API key in `app.py` as per initial setup instructions. **This is highly insecure for any real deployment.**

    **Recommended approach for local development/testing:**
    Set it as an environment variable:
    ```bash
    export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
    On Windows:
    ```bash
    set GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
    The application `app.py` is structured to pick up this environment variable if the hardcoded one is removed or commented out.

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will start (by default on `http://127.0.0.1:5000/`). Open this URL in your web browser.

    You will see warnings in the console if the hardcoded API key is being used.

## Usage

1.  **Upload PDF:** Use the "Upload PDF" section to select and upload a PDF file.
2.  **Process:** The application will extract text from the PDF.
3.  **Chat:** If processing is successful and the Gemini API is configured, the chat interface will appear. You can ask questions about the PDF content.
4.  **Knowledge Base:**
    *   **Save:** Click "Save Current PDF to Knowledge Base" to save the extracted text.
    *   **Load:** Choose a previously saved knowledge base from the list and click "Load" to interact with its content.

## Running Tests

To run the unit tests:
```bash
python -m unittest discover -s tests
```
Ensure all dependencies are installed before running tests.

## Future Improvements / Considerations

*   **Advanced PDF Parsing:** Integrate libraries like `pdfplumber` for more robust text and image extraction (multimodal capabilities).
*   **Multimodal Chat:** Extend Gemini integration to use `gemini-pro-vision` for questions about images within the PDF.
*   **Robust Knowledge Base:**
    *   Implement vector embeddings for semantic search within knowledge bases.
    *   Allow management (deletion, merging) of knowledge bases.
*   **Error Handling:** More granular error handling and user feedback.
*   **Security:**
    *   **NEVER use hardcoded API keys in production.** Use environment variables, secrets management services, or configuration files that are not committed to version control.
    *   Input validation and sanitization.
*   **Scalability:** For production, consider using a production-grade WSGI server (e.g., Gunicorn, uWSGI) instead of Flask's built-in development server.
*   **Database:** For more persistent chat history or user management, integrate a database.
*   **Async Operations:** For long PDF processing or API calls, consider asynchronous tasks to avoid blocking the server.
*   **Deployment:** Containerize with Docker, deploy to cloud platforms (e.g., Google Cloud Run, AWS Elastic Beanstalk, Heroku).

## Deprecation Warnings
*   The application currently uses `datetime.datetime.utcnow()`, which is deprecated. This should be updated to `datetime.datetime.now(datetime.UTC)`. This change is minor and can be done by editing `app.py` (e.g., line 189 based on current code).
