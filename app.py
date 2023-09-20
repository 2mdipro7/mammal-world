from flask import Flask, render_template, request
from gradio_client import Client
import json

app = Flask(__name__)

# Initialize the Gradio client with your API URL
gradio_api_url = "https://dipro7-mammals-of-india.hf.space/"
gradio_client = Client(gradio_api_url)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # Assuming you receive two JSON file paths as a list
        result_paths = json.loads(request.form['result'])
        
        # Ensure that two paths are provided
        if len(result_paths) != 2:
            return render_template("error.html", error_message="Expected two result paths.")

        # Extract species and behavior result paths
        species_result_path, behavior_result_path = result_paths

        try:
            # Load the JSON content from the species result path
            with open(species_result_path, 'r') as species_json_file:
                species_json_data = json.load(species_json_file)
                print("Species JSON Data:", species_json_data)
                pred_label = species_json_data.get("label", "Species not predicted")
                confidences = species_json_data.get("confidences", [])
                confidence = max(confidences, key=lambda item: item.get("confidence", 0))["confidence"] * 100

            # Load the JSON content from the behavior result path
            with open(behavior_result_path, 'r') as behavior_json_file:
                behavior_json_data = json.load(behavior_json_file)
                print("Behavior JSON Data:", behavior_json_data)
                behavior_label = behavior_json_data.get("behavior", "Behavior not predicted")

            return render_template("result.html", pred_label=pred_label, confidence=confidence, behavior_label=behavior_label, result_paths=result_paths)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            error_message = f"Error reading JSON file: {e}"
            print(error_message)
            return render_template("error.html", error_message=error_message)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
