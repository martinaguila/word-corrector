from flask import Flask, render_template, request
from openai import OpenAI
client = OpenAI(api_key='')
import time

app = Flask(__name__)

def code_auto_correction(input_code):
    # Check for "exit" command
    if input_code.lower().strip() == 'exit':
        return 'exit'

    # Generate a prompt for the OpenAI API
    prompt = f"Correct the following Python code:\n\n{input_code}\n\nCorrected code:"

    # Make a request to the OpenAI API to get corrected code
    # response = client.completions.create(engine="text-davinci-003",
    # prompt=prompt,
    # temperature=0.7,
    # max_tokens=150,
    # top_p=1.0,
    # frequency_penalty=0.0,
    # presence_penalty=0.0)
    response = client.completions.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    # print("response",response)
    # Extract corrected code from the API response
    # corrected_code = response['choices'][0]['text'].strip()
    corrected_code = response.choices[0].text
    
    # print("xd",corrected_code,"xd")

    # Make a separate request to the OpenAI API to get comments
    comment_prompt = f"Provide comments on the corrections made in the code:\n\n{corrected_code}\n\nComments:"
    comments_response = client.completions.create(model="text-davinci-003",
    prompt=comment_prompt,
    temperature=0.7,
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0)

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

    # Your code_auto_correction function call goes here
    corrected_code, comments = code_auto_correction(input_code)

    return render_template('index.html', input_code=input_code, corrected_code=corrected_code, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
    while True:
        print("Enter Python code to be corrected (type 'exit' to end):")
        
        # Accept multiline user input until an empty line is entered
        input_code_lines = []
        line = input()
        while line:
            input_code_lines.append(line)
            line = input()

        if not input_code_lines:
            print("Ending session. Goodbye!")
            break

        # Combine input lines into a single string
        input_code = '\n'.join(input_code_lines)

        # Check for "exit" command
        if input_code.lower().strip() == 'exit':
            print("Ending session. Goodbye!")
            break

        # Display a typing animation before the response
        type_animation("Thinking...")

        # Get the corrected code and comments
        corrected_code, comments = code_auto_correction(input_code)

        # Display a typing animation before showing the results
        type_animation("Here is the corrected code:")

        # Print the results
        print("\nOriginal code:\n", input_code)
        if corrected_code == 'exit':
            print("Ending session. Goodbye!")
            break
        elif corrected_code == input_code:
            print("Great job! Your code is correct and doesn't require any corrections.")
        else:
            type_animation("\nCorrected code with comments:\n")
            type_animation(corrected_code)
            print("\n" + "="*40 + "\n")
            type_animation("Comments on corrections:\n")
            type_animation(comments)

        # Double line separation
        print("\n" + "="*40 + "\n" )

        # Typing animation for the prompt
        response = ''
        while response not in ['yes', 'no']:
            response = input("Do you want to correct another code? (yes/no): ").lower().strip()

        if response == 'no':
            print("Ending session. Goodbye!")
            break

        # Double line separation
        print("\n" + "="*40 + "\n" + "="*40 + "\n")
