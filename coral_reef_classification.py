import numpy as np
import streamlit as st
import ollama
import cv2
import google.generativeai as genai
from google.generativeai.types import ContentType
import io
import requests
import re
from keras.models import load_model
import tensorflow as tf
import base64

genai.configure(api_key="AIzaSyDKpZ2nAonxAWNA5ETi2TSoY5FhGQBkkYc")


def get_base64(png_file):
    """Convert an image file to a base64 encoded string."""
    try:
        with open(png_file, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image {png_file}: {e}")
        return None

def set_background(png_file):
    bin_str = get_base64(png_file)
    if not bin_str:
        return
    
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
        width: 100vw !important; 
        height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
# Set the background image
# set_background("D:/Final Year Project/Coral Reef Sustainability/images/background3.jpg")
#C:/Users/vinot/My ML Projects/Medicinal Plants Classifcation/Implementation/Test Image/Tropical-Photography-Background-Wallpaper-119068.jpg

def run_page():
    set_background("D:/Final Year Project/Coral Reef Sustainability/images/backy1.jpg")
    st.title("CORAL REEF CLASSIFICATION")
    # st.write("Content for Coral Reef Classification page goes here.")
    model = load_model('D:/Project Phase 1/phase1model0.h5')
                        
    # Name of Classes
    CLASS_NAMES = ('Branching Coral', 'Sponge Coral','Brain coral')

    # Setting Title of App
    # st.title("Coral Ref Detection")
    st.write("Upload an image of the coral reef")

    # Uploading the coral image
    coral_image = st.file_uploader("Choose an image...", type = "jpg")
    submit = st.button('PREDICT CORAL REEF')

    # On predict button click
    if submit:
        if coral_image is not None:
            # Convert the file to an opencv image.
            file_bytes = np.asarray (bytearray(coral_image.read()), dtype = np.uint8)
            opencv_image = cv2.imdecode(file_bytes, 1)
            
            # Displaying the image
            st.image(opencv_image, channels="BGR")
            st.write(opencv_image.shape)
            
            # Resizing the image
            opencv_image = cv2.resize(opencv_image, (150, 150))
            
            # Convert image to 4 Dimension
            opencv_image.shape = (1, 150, 150, 3)
            
            #Make Prediction
            Y_pred = model.predict(opencv_image)
            result = CLASS_NAMES[np.argmax(Y_pred)]
            st.title(str("This coral reef is " +  result))

            # placeholder = st.empty()
            # placeholder.text("Gemini ai api additional details...")
            # gen_model = genai.GenerativeModel('gemini-1.5-pro-latest')
            # prompt = f"Please provide information about the coral reef: {result}"
            # response = gen_model.generate_content(prompt)
            # prompt2 = f"Please provide the products(along with buying link-do not give i cant provide link) related to coral reef: {result}"
            # response2 = gen_model.generate_content(prompt2)
            
            # placeholder.empty()
            # # Display the response in Streamlit
            # st.subheader(result+" Details:")
            # st.write(response.text)
            # st.write(response2.text)
            st.markdown("""
    <style>
        .content-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)
            placeholder1 = st.empty()
            placeholder1.text("Generating additional details...")

            # **Using Ollama's DeepSeek for text generation**stre
            prompt_info = f"Provide detailed information about the coral reef: {result}."
            response_info = ollama.chat(model="deepseek-r1:1.5b", messages=[{"role": "user", "content": prompt_info}])
            cleaned_text = re.sub(r"<think>.*?</think>", "", response_info['message']['content'], flags=re.DOTALL).strip()

            st.subheader(f"{result} Details:")
            placeholder1.empty()
            
            st.markdown(cleaned_text)

