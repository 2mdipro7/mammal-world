import streamlit as st
from gradio_client import Client
import tempfile
import json
import pandas as pd
import time

#import pathlib
#temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath

# Initialize Streamlit session state if not already initialized
#if 'initialized' not in st.session_state:
    #st.session_state.initialized = True
    #st.session_state.predictions = {}

# Load the data from the CSV file
data = pd.read_csv('data/data.csv')

# Import necessary libraries
import streamlit as st
import json
import tempfile
import time
from gradio_client import Client

# Initialize the Gradio client
gradio_api_url = "https://dipro7-mammals-of-india.hf.space/"
client = Client(gradio_api_url, api_name="/predict")

st.title("Mammal World - AI for Wildlife in India")

uploaded_image = st.sidebar.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

# Create a sidebar option for selecting input method
input_method = st.sidebar.radio("Select Input Method", ("Image Upload", "Text Description"))

if input_method == "Image Upload" and uploaded_image is not None:
    st.sidebar.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    
    # Create a temporary file to store the image
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_image.read())

    # Show a progress bar while the image is being uploaded
    progress_bar_upload = st.progress(0)
    with st.spinner("Uploading Image..."):
        for percent_complete in range(100):
            time.sleep(0.02)  # Simulate upload time (adjust as needed)
            progress_bar_upload.progress(percent_complete + 1)

    # Make a prediction using the Gradio client
    with st.spinner("Making Prediction..."):
        result = client.predict(temp_file.name)

    # Clear the spinner
    st.spinner(None)  # This will remove the spinner once prediction is done

    # Check if the response is a file path and read its content
    if isinstance(result, tuple) and len(result) == 2:
        species_prediction_json_path, behavior_prediction_json_path = result

        # Print the paths for debugging
        print("Species Prediction JSON Path:", species_prediction_json_path)
        print("Behavior Prediction JSON Path:", behavior_prediction_json_path)

        # Load and process species prediction JSON
        try:
            with open(species_prediction_json_path, 'r') as species_json_file:
                species_json_data = json.load(species_json_file)

            pred_label = species_json_data.get("label", "Species not predicted")
            confidences = species_json_data.get("confidences", [])

            if confidences:
                confidence = max(confidences, key=lambda item: item.get("confidence", 0))["confidence"] * 100
            else:
                confidence = 0
        except (FileNotFoundError, json.JSONDecodeError):
            st.write("Error: Invalid response format for species prediction.")
            pred_label = "Error"
            confidence = 0

        # Load and process behavior prediction JSON
        try:
            with open(behavior_prediction_json_path, 'r') as behavior_json_file:
                behavior_json_data = json.load(behavior_json_file)

            behavior_label = behavior_json_data.get("behavior", "Behavior not predicted")
            behavior_confidences = behavior_json_data.get("confidences", [])

            if behavior_confidences:
                behavior_confidence = max(behavior_confidences, key=lambda item: item.get("confidence", 0))["confidence"] * 100
            else:
                behavior_confidence = 0
        except (FileNotFoundError, json.JSONDecodeError):
            st.write("Error: Invalid response format for behavior prediction.")
            behavior_label = "Error"
            behavior_confidence = 0

        # Create a colored box for the prediction result
        prediction_result = f'<div style="background-color: #34ebcc; padding: 10px; border-radius: 5px;">' \
                            f'<strong>Prediction: {pred_label}</strong>' \
                            f'<br>We are {confidence:.2f}% confident it is a <i>{pred_label}</i></div>'
        
        # Create a colored box for the behavior prediction
        behavior_result = f'<div style="background-color: #89e8d8; padding: 10px; border-radius: 5px;">' \
                        f'<strong>Predicted Behavior:</strong> {behavior_label}</div>'

        # Render the prediction and behavior results using st.markdown
        st.markdown(prediction_result, unsafe_allow_html=True)
        st.markdown(behavior_result, unsafe_allow_html=True)

        # Define background colors for conservation status categories
        status_colors = {
            "Not Evaluated": "#FF5733",  # Red
            "Data Deficient": "#FFA500",  # Orange
            "Least Concern": "#32CD32",  # Green
            "Near Threatened": "#FFFF00",  # Yellow
            "Vulnerable": "#FF4500",  # Orange-Red
            "Endangered": "#FF0000",  # Bright Red
            "Critically Endangered": "#8B0000",  # Dark Red
            "Extinct in the Wild": "#800080",  # Purple
            "Extinct": "#000000",  # Black
        }

        # Retrieve the conservation status from the loaded DataFrame
        conservation_status = data[data['SpeciesName'] == pred_label]['Conservation Status'].values[0]

        # Get the background color based on the conservation status
        background_color = status_colors.get(conservation_status, "#FFFFFF")  # Default to white if not found

        # Create a colored box for the conservation status based on the background color
        conservation_result = f'<div style="background-color: {background_color}; padding: 10px; border-radius: 5px;">' \
                            f'<strong>Conservation Status:</strong> {conservation_status}</div>'

        st.markdown(conservation_result, unsafe_allow_html=True)

        # Fetch additional information from the CSV file based on the predicted label
        try:
            species_info = data[data['SpeciesName'] == pred_label]

            if not species_info.empty:
                st.header("Additional Information:")

                # Display selected columns in the sidebar as a vertical table with "Taxonomy" header
                sidebar_columns = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
                sidebar_data = species_info[sidebar_columns].T  # Transpose the DataFrame
                sidebar_data.columns = ["Taxonomy"]  # Set "Taxonomy" as the header

                # Create HTML code to style the taxonomy table
                table_html = f'<div style="width: 300px; margin: 0 auto;">'
                table_html += f'<table style="width: 100%; text-align: center;">'

                # Table header for the taxonomy table
                table_html += f'<tr>'
                table_html += f'<th colspan="2" style="background-color: #f2f2f2;">Taxonomy</th>'
                table_html += f'</tr>'

                # Table rows for the taxonomy table
                for index, row in sidebar_data.iterrows():
                    table_html += f'<tr>'
                    table_html += f'<td style="width: 50%; text-align: left;"><strong>{index}:</strong></td>'
                    table_html += f'<td style="width: 50%; text-align: left;">{row.values[0]}</td>'
                    table_html += f'</tr>'

                table_html += f'</table>'
                table_html += f'</div>'

                # Render the styled taxonomy table using st.markdown
                st.markdown(table_html, unsafe_allow_html=True)

                # Assuming you have a DataFrame called 'species_info' with the 'CommonNames' column

                # Now, iterate through other columns and display their data
                columns_to_display = ['Overview', 'Size', 'Morphology', 'Distribution', 'Habitat', 'Habitat Details']

                for column in columns_to_display:
                    if column in species_info.columns:
                        st.subheader(column)
                        st.write(species_info[column].values[0])
                    else:
                        st.write(f"No {column} information found for the predicted species.")
            else:
                st.write("No additional information found for the predicted species.")
        except IndexError:
            st.write("Error: Invalid response from the API or no matching data found.")


else:
    # Display the introductory content when no input is provided
    st.write("Welcome to Mammal World - AI for Wildlife in India")
    st.subheader("About Us:")
    st.write("At Mammal World, we're using AI to protect India's diverse wildlife. Join us in exploring, understanding, and conserving these incredible species.")
    st.subheader("AI Species Identification:")
    st.write("Discover 103 mammal species with our AI model.")
    st.write("See how AI is transforming wildlife conservation.")
    st.subheader("Explore Wildlife Behaviors:")
    st.write("Understand animal interactions, mating, feeding, and more.")
    st.write("Stay informed about conservation efforts.")
    st.subheader("Educate and Advocate:")
    st.write("Access educational resources and interactive content.")
    st.write("Join our community of wildlife enthusiasts.")
    st.subheader("Real-Time Monitoring:")
    st.write("Witness AI-powered real-time analysis.")
    st.write("Help protect wildlife from threats.")
    st.subheader("Join the Wildlife Revolution:")
    st.write("Start exploring the beauty of India's wildlife.")
    st.write("Together, we can make a difference.")
    st.subheader("Our Vision: AI for Wildlife, Conservation for All.")

footer_html = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f8f8f8;
    text-align: center;
    padding: 5px;
    font-size: 12px;
}
</style>
<div class="footer">
    This project is created by Mehrab Mashrafi under MIT License.
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)


