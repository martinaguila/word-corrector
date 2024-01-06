from flask import Flask, render_template, request
from openai import OpenAI
from pygments.lexers import guess_lexer

client = OpenAI(api_key='')
import time

app = Flask(__name__)

def code_auto_correction(input_code, language):
    # Check for "exit" command
    if input_code.lower().strip() == 'exit':
        return 'exit'

    # Generate a prompt for the OpenAI API
    prompt = f"Correct the following {language} code:\n\n{input_code}\n\nCorrected code:"

    # Make a request to the OpenAI API to get corrected code
    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract corrected code from the API response
    corrected_code = response.choices[0].text

    # Make a separate request to the OpenAI API to get comments
    comment_prompt = f"Provide comments on the corrections made in the code:\n\n{corrected_code}\n\nComments:"
    comments_response = client.completions.create(
        model="text-davinci-003",
        prompt=comment_prompt,
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract comments from the API response
    comments = comments_response.choices[0].text

    return corrected_code, comments

# Function for typing animation
def type_animation(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Move to the next line after the animation


@app.route('/')
def home():
    return render_template('index.html', input_code="", corrected_code="", comments="")

@app.route('/submit', methods=['POST'])
def submit():
    input_code = request.form['code_input']

    # Determine the language of the code
    language = guess_lexer(input_code).name
    print("language",language)
    # Your code_auto_correction function call goes here
    corrected_code, comments = code_auto_correction(input_code, language)

    return render_template('index.html', input_code=input_code, corrected_code=corrected_code, comments=comments, language=language)

if __name__ == '__main__':
    app.run(debug=True)
