import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()  # the function will take & load the values from .env.




from flask import Flask, redirect, url_for, request, render_template, session
app = Flask(__name__)


'''
open new terminal to run
> python -m flask run

>to create the project database, open terminal
- type python and press enter
- type 
    from app import app, db
    with app.app_context():
        db.create_all()
- enter twice to confirm

>ctrl+c to stop the flask server
'''





@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form
    # 1. Reads the text the user entered and the language they selected on the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    # 2. Reads the environmental variables we created earlier from our .env file
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # 3. Creates the necessary path to call the Translator service, 
    #    which includes the target language (the source language is automatically detected)

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Make the call using "post" on "requests" and pass in the URL, headers, and body
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response from the server, which includes the translated text
    translator_response = translator_request.json()
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render_template to display response page, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )