import streamlit as st
from openai import OpenAI
import base64
import os
import datetime




@st.dialog("Cast your vote")
def vote():
    
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)

    if picture:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"image_{timestamp}.png"

        with open(file_path, "wb") as file:
            file.write(picture.getbuffer())

        # Save the image to the specified folder
        with open(file_path, "rb") as image_file:
             st.session_state.img = base64.b64encode(image_file.read()).decode('utf-8')
        
        st.rerun()


if st.sidebar.button("take image"):
    vote()

client = OpenAI(api_key=st.secrets['openai_key'])
system_message = '''
You are a bot 
'''
# Show title and description.
st.title( "MY Lab3 question answering chatbot")

model_to_use = "gpt-4o-mini"


# Create an OpenAI client.


# Getting the base64 string

if "img" in st.session_state:
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What is in this image?",
            },
            {
            "type": "image_url",
            "image_url": {
                "url":  f"data:image/jpeg;base64,{st.session_state.img}"
            },
            },
        ],
        }
    ],
    stream = True
    )
    st.write_stream(response)
