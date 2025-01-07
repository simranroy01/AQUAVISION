import streamlit as st
from PIL import Image
from ultralytics import YOLO
import os
import tempfile
import numpy as np

# Load the YOLO model
model_path = r'D:\projjjj\WaterWaste\training_results\plastic6\weights\best.pt'
model = YOLO(model_path)

# Streamlit App UI
st.title("Plastic Waste Detection")
st.write("Upload an image to detect plastic waste.")

# File upload widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Open and display the uploaded image
    img = Image.open(uploaded_file)

    # Convert RGBA images to RGB
    if img.mode == "RGBA":
        img = img.convert("RGB")

    st.image(img, caption="Uploaded Image.", use_column_width=True)

    # Save the uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        input_image_path = temp_file.name
        img.save(input_image_path)

    # Make predictions with the YOLO model
    st.write("Running model prediction...")
    results = model(input_image_path)

    # Debugging: Print results details
    st.write("Results Object:", results)
    st.write("Save Directory:", results[0].save_dir)

    # Visualize the prediction results (bounding boxes and labels)
    annotated_img = results[0].plot()  # This method draws bounding boxes and labels on the image

    # Convert the annotated image to a format that can be saved
    annotated_img_pil = Image.fromarray(annotated_img)  # Convert numpy array to PIL image

    # Define the path where you want to save the result image within your project
    result_image_dir = r'D:\projjjj\WaterWaste\result_images'

    # Create the directory if it doesn't exist
    if not os.path.exists(result_image_dir):
        st.write(f"Creating save directory: {result_image_dir}")
        os.makedirs(result_image_dir)

    # Manually save the result image after prediction
    result_image_path = os.path.join(result_image_dir, f"result_{os.path.basename(input_image_path)}")
    annotated_img_pil.save(result_image_path)
    st.write(f"Image saved at: {result_image_path}")

    # Check if the image exists and display it
    if os.path.exists(result_image_path):
        st.image(result_image_path, caption="Prediction Result", use_column_width=True)
    else:
        st.error("Result image not found!")
        st.write(f"Expected Path: {result_image_path}")
        st.write("Check the model save directory and permissions.")

    # Clean up the temporary file
    os.remove(input_image_path)
