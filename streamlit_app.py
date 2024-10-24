from openai import OpenAI
import streamlit as st
import base64

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
image_path = "k2xnp9yctuw91.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

st.session_state.client = OpenAI(api_key=st.secrets['openai_key'])

stream = st.session_state.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}",
            "detail": "high"
          },
        },
      ],
    }
  ],
        stream=True
    )

st.write_stream(stream)

