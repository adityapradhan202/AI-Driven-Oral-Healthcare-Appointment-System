import streamlit as st
import os
from PIL import Image
import requests
import time

with st.sidebar:
    phone = st.text_input(label='Phone number here', value="+91")
    name = st.text_input(label='Enter your name here', value='Name here')
    age = st.slider(label='What is your age?', min_value=5, max_value=80, value=5)          
    address = st.text_input(label='Enter your address here', value='Address here')
    gender = st.radio(label="Choose your gender", options=['Male', 'Female'], index=None)

    st.write("Refresh the page, if you want to clear the entries.")
    


st.write('Make sure to enter all the personal information given on the left sidebar before proceeding...')
uploaded_image = st.file_uploader(label='Upload an image of your teeth', type=['jpg', 'jpeg', 'png'])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=False)

    temp_folder = "temp_files"
    os.makedirs(temp_folder, exist_ok=True)
    temp_file_path = os.path.join(temp_folder, "temp_image.jpg")
    image.save(temp_file_path)

    with st.spinner(text='Model is analysing, wait for a few seconds'):
        time.sleep(2)
        api_url = "http://127.0.0.1:5000/predict"  # Replace with your deployed Flask API URL
        with open(temp_file_path, 'rb') as file:
            response = requests.post(api_url, files={'file': file})

        if response.status_code == 200:
            result = response.json()
            st.write(result)
        else:
            st.write('Some error occured!')



    
