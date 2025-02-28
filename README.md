# CDP_CHAT-BOT
This project implements a chatbot that answers "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot leverages the official documentation of these CDPs to provide relevant answers to user queries. It includes a Python Flask backend for processing and an HTML/CSS/JavaScript frontend for the user interface.

The project is organized into the following files and directories:
cdp_chatbot/ ├── app.py (Python Flask backend)
index.html (HTML frontend) 
style.css (CSS stylesheet) 
script.js (JavaScript logic) 

Technologies used:

1. Frontend:
HTML: For structuring the user interface.
CSS: For styling the user interface.
JavaScript: For handling user interactions, making requests to the backend, and updating the UI dynamically.

2. Backend:
Python: Programming language for the backend logic.
Flask: Micro web framework for creating the API.
Requests: Library for making HTTP requests to scrape documentation.
Beautiful Soup 4 (bs4): Library for parsing HTML content.
Sentence Transformers: Library for generating text embeddings.
FAISS: Library for efficient similarity search of embeddings.
Numpy: Numerical library for python, to perform calculations of embedding vectors.
NLTK: Text processing library, to help with tokenization.


HOW TO USE?

1. Prerequisites:
Python 3.6+: Make sure you have Python 3.6 or higher installed.
pip: Python package manager.
Virtual Environment (recommended)
All required python packages: Install all python dependencies using pip install -r requirements.txt. A requirements.txt example is:
requests beautifulsoup4 sentence-transformers faiss-cpu numpy flask flask-cors nltk .

2. Setup:

Create a project directory: Create a new directory for your project, for example cdp-chatbot
Create python files:
Create an app.py file, copy the code from the python section above and paste into it.
Create the frontend files: Create an index.html, style.css and script.js and paste the code provided above.
Install dependencies: Open your terminal, navigate to the folder, and run pip install -r requirements.txt.
Start the python server: Run the app.py file using python app.py. The python server should start and listen to http://localhost:5500

3. Running:

Open the index.html file in your web browser.
Type your question in the chat input field.
Press the "Send" button to send the question to the server.
The chatbot's response (or error message) will appear in the chat history, with source links when possible.

4. Errors and Troubleshoots:

   Error Handling: If you are getting ModuleNotFoundError errors, make sure you have correctly installed all packages.

    Python packages: If you are having any problem running the python server, please check the previous steps about resolving ModuleNotFoundError, make sure your pip is updated, and try installing all the python packages one by one.
   
   CORS Errors: If you have any CORS errors, check that your browser is not blocking cross-origin requests.

   Network Issues: If you are getting network errors, make sure your internet connection is working correctly.


