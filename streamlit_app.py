import streamlit as st
from openai import OpenAI
import base64
import os
import datetime
from io import BytesIO
from PIL import Image


st.title( "MY Lab3 question answering chatbot")


system_message = '''
You are a bot 
'''


if 'client' not in st.session_state:
    st.session_state.client = OpenAI(api_key=st.secrets['openai_key'])

if "messages" not in st.session_state:
    st.session_state["messages"] = \
    [{"role": "system", "content": system_message},
     {"role": "assistant", "content": "How can I help you?"}]
    

@st.dialog("Take a Photo")
def cam():
    
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)
    preprocess(picture)





def preprocess(picture):

    if picture:
        st.session_state.show_img = picture
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"image_{timestamp}.png"

        with open(file_path, "wb") as file:
            file.write(picture.getbuffer())

        with open(file_path, "rb") as image_file:
             st.session_state.img = base64.b64encode(image_file.read()).decode('utf-8')
        
        st.rerun()



if st.sidebar.button("Camera 📷"):
    cam()

st.session_state.uploaded_file = st.sidebar.file_uploader(
    "Upload a photo", type=("jpg", "png"))

if st.sidebar.button("Upload files ⬆️"):
    preprocess(st.session_state.uploaded_file)


if "show_img" in st.session_state:
    st.sidebar.image(st.session_state.show_img)

for msg in st.session_state.messages:
    if msg["role"] != "system":
        if isinstance(msg["content"], list) and len(msg["content"]) > 1:
            if msg["content"][1].get("type") == "image_url":
                col1, col2 = st.columns([1, 3])
                img_data = base64.b64decode(msg["content"][1]["image_url"]["url"].split(",")[1])
                col1.image(img_data)
                chat_msg = st.chat_message(msg["role"]) 
                chat_msg.write(msg["content"][0].get("text"))
        else:
            chat_msg = st.chat_message(msg["role"]) 
            chat_msg.write(msg["content"])

if prompt := st.chat_input("What is up?"):
    if "show_img" in st.session_state:
        del st.session_state["show_img"]
    st.rerun()
    if "img" in st.session_state:
        col1, col2 = st.columns([1, 3])
        img_data = base64.b64decode(st.session_state.img)
        col1.image(img_data)
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content":[
        {"type": "text", "text": prompt},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{st.session_state.img}",
          },
        },
      ]})
        del st.session_state["img"]
        

    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


    client = st.session_state.client
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        stream=True
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})