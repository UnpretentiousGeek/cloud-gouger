from openai import OpenAI
import streamlit as st

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
            "url": "k2xnp9yctuw91.jpg",
            "detail": "high"
          },
        },
      ],
    }
  ],
        stream=True
    )

st.write_stream(stream)

