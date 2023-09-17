import streamlit as st
from gradio_client import Client
import io
import tempfile
import json
import pandas as pd
import joblib
from fastai.vision.all import *

#import pathlib
#temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath

# Load the data from the CSV file
data = pd.read_csv('data/data.csv')

# Load your pre-trained behavior prediction model
model = load_learner('behavior_model_v1.pkl')

# Initialize the Gradio client
gradio_api_url = "https://dipro7-mammals-of-india.hf.space/"
client = Client(gradio_api_url)

st.title("Mammal World - AI for Wildlife in India")

# Load your pre-trained text classification model
text_classifier_model = joblib.load('text_classifier_model.pkl')

# Load the CountVectorizer used during training
with open('count_vectorizer.pkl', 'rb') as vectorizer_file:
    count_vectorizer = joblib.load(vectorizer_file)

uploaded_image = st.sidebar.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

# Create a sidebar option for selecting input method
input_method = st.sidebar.radio("Select Input Method", ("Image Upload", "Text Description"))

if input_method == "Image Upload" and uploaded_image is not None:
    st.sidebar.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    
    # Create a temporary file to store the image
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_image.read())

    # Make a prediction using the Gradio client
    result = client.predict(temp_file.name, api_name="/predict")

    # Check if the response is a file path and read its content
    if isinstance(result, str):
        with open(result, 'r') as json_file:
            json_data = json.load(json_file)

        if "label" in json_data and "confidences" in json_data:
            pred_label = json_data["label"]
            confidences = json_data["confidences"]
            confidence = max(confidences, key=lambda item: item["confidence"])["confidence"] * 100

            # Create a colored box for the prediction result
            prediction_result = f'<div style="background-color: #FAD02E; padding: 10px; border-radius: 5px;">' \
                                f'<strong>Prediction: {pred_label}</strong>' \
                                f'<br>We are {confidence:.2f}% confident it is a {pred_label}</div>'
            
            # Render the prediction result using st.markdown
            st.markdown(prediction_result, unsafe_allow_html=True)

            # Predict behavior using the same image with the behavior model
            img = PILImage.create(temp_file.name)
            behavior_prediction, _, _ = model.predict(img)

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

            # Create a colored box for the behavior prediction and conservation status
            behavior_result = f'<div style="background-color: #FFA07A; padding: 10px; border-radius: 5px;">' \
                            f'<strong>Predicted Behavior:</strong> {behavior_prediction[0]}</div>'
            

            # Render the behavior prediction result using st.markdown
            st.markdown(behavior_result, unsafe_allow_html=True)

            st.markdown(conservation_result, unsafe_allow_html=True)

            # Fetch additional information from the CSV file based on the predicted label
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
                columns_to_display = ['Overview', 'Size', 'Morphology', 'Behavior', 'Distribution', 'Habitat', 'Habitat Details']

                for column in columns_to_display:
                    if column in species_info.columns:
                        st.subheader(column)
                        st.write(species_info[column].values[0])
                    else:
                        st.write(f"No {column} information found for the predicted species.")
            else:
                st.write("No additional information found for the predicted species.")
        else:
            st.write("Error: Invalid response format in the JSON file.")
    else:
        st.write("Error: Invalid response from the API.")

elif input_method == "Text Description":
    st.sidebar.subheader("Text Description")
    
    with st.sidebar.form("animal_description_form"):
        text_description = st.text_area("Describe an animal:")
        submit_button = st.form_submit_button("Predict")
    
    if submit_button:
        text_description = text_description.strip()
        text_description_2d = [text_description]  # Convert to a 2D list
        text_description_vector = count_vectorizer.transform(text_description_2d)
        predicted_label = text_classifier_model.predict(text_description_vector)[0]

        st.write(f"Predicted Animal: {predicted_label}")

        species_info = data[data['SpeciesName'] == predicted_label]

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

            # Display Common Names

            # Now, iterate through other columns and display their data
            columns_to_display = ['Overview', 'Size', 'Morphology', 'Behavior', 'Distribution', 'Habitat', 'Habitat Details']

            for column in columns_to_display:
                if column in species_info.columns:
                    st.subheader(column)
                    st.write(species_info[column].values[0])
                else:
                    st.write(f"No {column} information found for the predicted species.")
        else:
            st.write("No additional information found for the predicted species.")

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

