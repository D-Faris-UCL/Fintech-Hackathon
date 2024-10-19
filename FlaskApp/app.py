from flask import Flask, render_template, request
import script  # Import your script

app = Flask(__name__)

@app.route('/')
def index():
    # HTML template for the homepage
    return render_template("index.html")

@app.route('/run_script', methods=['POST'])
def run_script():
    # Call the main function from script.py
    output = script.main()
    # Render the output in the web page
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Script Output</title>
        </head>
        <body>
            <h1>Output of the Script:</h1>
            <pre>{output}</pre>
            <a href="/">Go Back</a>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True,port=5001)