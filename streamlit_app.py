import streamlit as st

if "img" in st.session_state:
    col1, col2 = st.columns([3, 1])
    col2.image(st.session_state.img)

@st.dialog("Cast your vote")
def vote():
    
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)
    if picture:
        st.session_state.img = picture
        st.rerun()


if st.button("take image"):
    vote()