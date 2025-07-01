import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import json
import shutil # Import shutil for rmtree

# Add the parent directory to the Python path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, extract_text_from_pdf, GOOGLE_API_KEY

class BasicAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing forms if any
        self.upload_folder = tempfile.mkdtemp()
        self.kb_folder = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.upload_folder
        app.config['KNOWLEDGE_BASE_FOLDER'] = self.kb_folder
        self.client = app.test_client()

        # Ensure API key is set for tests that might depend on Gemini initialization
        # If GOOGLE_API_KEY is not the one from the prompt, tests needing it might behave differently
        # For unit tests, we often mock the API interaction itself.
        self.google_api_key = GOOGLE_API_KEY
        if not self.google_api_key:
            print("WARNING: GOOGLE_API_KEY not found for testing. Some tests might be skipped or fail if they rely on real API configuration.")

        # Mock PyPDF2 and Gemini API for most tests to avoid external dependencies
        self.pdf_reader_patch = patch('app.PyPDF2.PdfReader')
        self.mock_pdf_reader = self.pdf_reader_patch.start()

        self.genai_patch = patch('app.genai')
        self.mock_genai = self.genai_patch.start()
        # Configure the mock genai.GenerativeModel
        self.mock_gemini_model_instance = MagicMock()
        self.mock_genai.GenerativeModel.return_value = self.mock_gemini_model_instance


    def tearDown(self):
        self.pdf_reader_patch.stop()
        self.genai_patch.stop()
        # Clean up temporary directories using shutil.rmtree
        shutil.rmtree(self.upload_folder)
        shutil.rmtree(self.kb_folder)


    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Gemini PDF Parser", response.data)
        # Check if Gemini was initialized (mocked as successful)
        if self.google_api_key: # Only assert if key is expected to be present
             self.assertIn(b"Chat with PDF", response.data) # Chat section should be potentially visible
        else:
            self.assertIn(b"Warning: GOOGLE_API_KEY not provided", response.data)

    def test_pdf_upload_and_extraction(self):
        # Mock the PDF content
        mock_pdf_page = MagicMock()
        mock_pdf_page.extract_text.return_value = "This is test PDF content."
        self.mock_pdf_reader.return_value.pages = [mock_pdf_page]

        # Create a dummy PDF file for upload
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
            tmp_pdf.write(b"dummy pdf content") # Actual content doesn't matter due to mocking
            self.test_pdf_path = tmp_pdf.name

        with open(self.test_pdf_path, 'rb') as fp:
            data = {'file': (fp, 'test.pdf')}
            response = self.client.post('/upload', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 302) # Redirects to index
        with self.client.session_transaction() as sess:
            self.assertTrue(sess['pdf_processed'])
            self.assertEqual(sess['pdf_filename'], 'test.pdf')
            self.assertEqual(sess['pdf_text'], "This is test PDF content.")

        # Clean up the dummy file
        os.remove(self.test_pdf_path)

    def test_chat_route_success(self):
        # Ensure Gemini model is mocked to return a response
        mock_chat_session = MagicMock()
        mock_chat_session.send_message.return_value.text = "Mocked Gemini reply"
        self.mock_gemini_model_instance.start_chat.return_value = mock_chat_session

        with self.client.session_transaction() as sess:
            sess['pdf_processed'] = True
            sess['pdf_text'] = "Some PDF text"
            sess['pdf_filename'] = "test.pdf"
            sess['chat_history'] = []
            sess['gemini_initialized'] = True # Crucial for chat route to proceed

        response = self.client.post('/chat', json={'message': 'Hello Gemini'})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['reply'], "Mocked Gemini reply")
        with self.client.session_transaction() as sess:
            self.assertEqual(len(sess['chat_history']), 2)
            self.assertEqual(sess['chat_history'][0]['text'], 'Hello Gemini')
            self.assertEqual(sess['chat_history'][1]['text'], 'Mocked Gemini reply')


    def test_chat_route_pdf_not_processed(self):
        with self.client.session_transaction() as sess:
            sess['pdf_processed'] = False
            sess['gemini_initialized'] = True
        response = self.client.post('/chat', json={'message': 'Hello?'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"PDF not processed", response.data)

    def test_chat_route_gemini_not_initialized(self):
        with self.client.session_transaction() as sess:
            sess['pdf_processed'] = True
            sess['pdf_text'] = "Some PDF text"
            sess['gemini_initialized'] = False # Simulate Gemini init failure
        response = self.client.post('/chat', json={'message': 'Hello?'})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Gemini API not initialized", response.data)


    def test_save_knowledge_base(self):
        pdf_name = "my_document.pdf"
        pdf_content = "This is the content of my document."
        with self.client.session_transaction() as sess:
            sess['pdf_processed'] = True
            sess['pdf_filename'] = pdf_name
            sess['pdf_text'] = pdf_content

        response = self.client.post('/save_kb')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])
        saved_kb_filename = json_data['kb_name']
        self.assertEqual(saved_kb_filename, pdf_name + ".json")

        # Verify the file was created and contains correct data
        kb_filepath = os.path.join(app.config['KNOWLEDGE_BASE_FOLDER'], saved_kb_filename)
        self.assertTrue(os.path.exists(kb_filepath))
        with open(kb_filepath, 'r') as f:
            kb_data = json.load(f)
        self.assertEqual(kb_data['original_filename'], pdf_name)
        self.assertEqual(kb_data['text_content'], pdf_content)
        os.remove(kb_filepath) # Clean up

    def test_load_knowledge_base(self):
        kb_name = "sample_kb.pdf.json"
        kb_data_content = {
            'original_filename': "sample_kb.pdf",
            'text_content': "Content from knowledge base."
        }
        # Create a dummy KB file
        kb_filepath = os.path.join(app.config['KNOWLEDGE_BASE_FOLDER'], kb_name)
        with open(kb_filepath, 'w') as f:
            json.dump(kb_data_content, f)

        response = self.client.post('/load_kb', json={'kb_name': kb_name})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['pdf_filename'], kb_data_content['original_filename'])

        with self.client.session_transaction() as sess:
            self.assertTrue(sess['pdf_processed'])
            self.assertEqual(sess['pdf_filename'], kb_data_content['original_filename'])
            self.assertEqual(sess['pdf_text'], kb_data_content['text_content'])
            self.assertEqual(sess['chat_history'], [])
        os.remove(kb_filepath) # Clean up

    def test_extract_text_from_pdf_mocked(self):
        # This directly tests the utility function with PyPDF2 mocked
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Extracted page text. "
        self.mock_pdf_reader.return_value.pages = [mock_page, mock_page] # Two pages

        # Create a dummy file path (doesn't need to be a real PDF due to mocking)
        dummy_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], "dummy.pdf")
        with open(dummy_pdf_path, "w") as f: # Create an empty file
            f.write("")

        extracted_text = extract_text_from_pdf(dummy_pdf_path)
        self.assertEqual(extracted_text, "Extracted page text. Extracted page text. ")
        self.mock_pdf_reader.assert_called_once() # Ensure PdfReader was called
        os.remove(dummy_pdf_path)


if __name__ == '__main__':
    # Create tests directory if it doesn't exist for test runner
    if not os.path.exists('tests'):
        os.makedirs('tests')
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

# To run these tests:
# 1. Ensure you are in the root directory of the project.
# 2. Run `python -m unittest discover -s tests` or `python tests/test_app.py`
#    (if test_app.py is made executable and has the shebang).
#    For the `discover` command to work, `tests` should be a package (have an __init__.py).
#    Let's add a simple __init__.py for that.
