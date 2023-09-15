import streamlit as st
from gradio_client import Client
import io
import tempfile
import json
import pandas as pd
import joblib

# Load the data from the CSV file
data = pd.read_csv('data/data.csv')

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
    if isinstance(result, str) and result.startswith("C:"):
        with open(result, 'r') as json_file:
            json_data = json.load(json_file)

        if "label" in json_data and "confidences" in json_data:
            pred_label = json_data["label"]
            confidences = json_data["confidences"]
            st.write(f"Prediction: {pred_label}")
            st.write("Confidences:")
            for item in confidences:
                label = item["label"]
                confidence = item["confidence"]
                st.write(f"{label}: {confidence:.4f}")

            # Fetch additional information from the CSV file based on the predicted label
            species_info = data[data['SpeciesName'] == pred_label]

            if not species_info.empty:
                st.write("Additional Information:")

                # Define columns to display
                columns_to_display = ['Overview', 'Size', 'Morphology', 'Behavior', 'Distribution', 'Habitat', 'Habitat Details', 'Conservation Status']

                for column in columns_to_display:
                    if column in species_info.columns:
                        st.subheader(column)
                        st.write(species_info[column].values[0])
                    else:
                        st.write(f"No {column} information found for the predicted species.")

                        # Display selected columns in the sidebar as a vertical table with "Taxonomy" header
                        sidebar_columns = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
                        sidebar_data = species_info[sidebar_columns].T  # Transpose the DataFrame
                        sidebar_data.columns = ["Taxonomy"]  # Set "Taxonomy" as the header
                        st.sidebar.write(sidebar_data)
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
            st.subheader("Additional Information:")
            # Define columns to display
            columns_to_display = ['Overview', 'Size', 'Morphology', 'Behavior', 'Distribution', 'Habitat', 'Habitat Details', 'Conservation Status']

            for column in columns_to_display:
                if column in species_info.columns:
                    st.subheader(column)
                    st.write(species_info[column].values[0])
                else:
                    st.write(f"No {column} information found for the predicted species.")

                    # Display selected columns in the sidebar as a vertical table with "Taxonomy" header
                    sidebar_columns = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
                    sidebar_data = species_info[sidebar_columns].T  # Transpose the DataFrame
                    sidebar_data.columns = ["Taxonomy"]  # Set "Taxonomy" as the header
                    st.sidebar.write(sidebar_data)
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
