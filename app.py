from flask import Flask, render_template, request, jsonify
import json
import os
import tempfile
from gradio_client import Client

app = Flask(__name__)

# Initialize the Gradio client with your API URL
gradio_api_url = "https://dipro7-mammals-of-india.hf.space/"
gradio_client = Client(gradio_api_url)

# Define a temporary directory to store prediction JSON files
temp_directory = tempfile.mkdtemp()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle URL input and make predictions using Gradio client
        image_url = request.form.get("image_url")

        if not image_url:
            return "No image URL provided"

        try:
            # Get predictions from the Gradio model using the provided URL
            result = gradio_client.predict({
                "image": image_url
            }, api_name="/predict")

            # Process the prediction result
            pred_label = result.get("label", "Species not predicted")
            confidences = result.get("confidences", [])
            confidence = max(confidences, key=lambda item: item.get("confidence", 0))["confidence"] * 100

            # Save prediction results to separate JSON files for species and behavior
            species_prediction_json_path = os.path.join(temp_directory, "species_prediction.json")
            behavior_prediction_json_path = os.path.join(temp_directory, "behavior_prediction.json")

            with open(species_prediction_json_path, 'w') as species_json_file:
                species_json_file.write(json.dumps(result))

            with open(behavior_prediction_json_path, 'w') as behavior_json_file:
                behavior_json_file.write(json.dumps(result))

            return jsonify({"message": "Prediction successful!", "pred_label": pred_label, "confidence": confidence})

        except Exception as e:
            return str(e)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
