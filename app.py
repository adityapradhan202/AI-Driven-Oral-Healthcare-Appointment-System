import streamlit as st
import os
from PIL import Image
import requests
import time

# Loading json
import json
with open('solutions.json', 'r') as file:
    solutions = json.load(file)

st.header(':orange[ORANN-V1]')
st.write('ORANN-V1 is an AI model that can make predictions about your oral health very precisely and accurately by harnessing the power of CNN models and NLP models. :green[Make sure to enter all the personal information given on the left sidebar before proceeding.]')


with st.sidebar:
    phone = st.text_input(label='Phone number here', value="+91")
    name = st.text_input(label='Enter your name here', value='Name here')
    age = st.slider(label='What is your age?', min_value=5, max_value=80, value=5)          
    address = st.text_input(label='Enter your address here', value='Address here')
    gender = st.radio(label="Choose your gender", options=['Male', 'Female'], index=None)

    st.write("Refresh the page, if you want to clear the entries.")

problem_description = st.text_area(
    "Enter your text below: (Required!!)", 
    value="Describe your problem here (Max 300 chars)", 
    height=150, 
    max_chars=300
)
    
uploaded_image = st.file_uploader(label='Upload an image of your teeth', type=['jpg', 'jpeg', 'png'])

temp_folder = "temp_files"
os.makedirs(temp_folder, exist_ok=True)

if uploaded_image and problem_description!= "Describe your problem here (Max 300 chars)":
    check_btn = st.button(label='Check results', type='primary')

    if check_btn:

        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=False)
        temp_file_path = os.path.join(temp_folder, "temp_image.jpg")
        image.save(temp_file_path)

        with st.spinner(text='Model is analysing, wait for a few seconds'):
            time.sleep(3)
            api_url = "http://127.0.0.1:5000/predict"  # Replace with your deployed Flask API URL
            with open(temp_file_path, 'rb') as file:
                response = requests.post(api_url, files={'file': file})

            if response.status_code == 200:
                result = response.json()
                st.markdown("#### :orange[Predictions done by the cnn pipeline:]")
                st.write(result)
            else:
                st.write('Some error occured!')
        
        # Solutions from the json
        specific_sol = solutions[result['EFFNET']]
        # st.write(specific_sol)

        st.markdown('#### :orange[Solutions:]')
        for key in specific_sol:
            time.sleep(0.25)
            st.write(f"▶️  {key}:")
            time.sleep(0.25)
            for index, sentence in enumerate(specific_sol[key]):
                st.write(f"{index+1}. {sentence}")

    
