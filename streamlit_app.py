import streamlit as st
from openai import OpenAI

@st.dialog("Cast your vote")
def vote():
    
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)
    if picture:
        st.session_state.img = picture
        st.rerun()


if st.sidebar.button("take image"):
    vote()


system_message = '''
You are a bot 
'''
# Show title and description.
st.title( "MY Lab3 question answering chatbot")

model_to_use = "gpt-4o-mini"


# Create an OpenAI client.
if 'client' not in st.session_state:
    st.session_state.client = OpenAI(api_key=st.secrets['openai_key'])

if "messages" and "messages2" not in st.session_state:
    st.session_state["messages"] = \
    [{"role": "system", "content": system_message},
     {"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        if isinstance(msg["content"], list) and len(msg["content"]) > 1:
            if msg["content"][1].get("type") == "image_url":
                col1, col2 = st.columns([3, 1])
                col2.image(msg["content"][1]["image_url"])
        else:
            chat_msg = st.chat_message(msg["role"]) 
            chat_msg.write(msg["content"])

if prompt := st.chat_input("What is up?"):
    if "img" in st.session_state:
        col1, col2 = st.columns([3, 1])
        col2.image(st.session_state.img)
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content":[
        {"type": "text", "text": prompt},
        {
          "type": "image_url",
          "image_url": {
            "url": st.session_state.img,
          },
        },
      ]})

    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


    client = st.session_state.client
    stream = client.chat.completions.create(
        model=model_to_use,
        messages=st.session_state.messages,
        stream=True
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})