# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from gradio_client import Client

app = Flask(__name__)

# Initialize the Gradio client
gradio_api_url = "https://dipro7-mammals-of-india.hf.space/"
gradio_client = Client(gradio_api_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file:
        # Save the uploaded image to a temporary location
        filename = secure_filename(file.filename)
        image_path = 'uploads/' + filename
        file.save(image_path)

        # Make a prediction using the Gradio client
        result = gradio_client.predict(image_path, api_name="/predict")

        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
