import streamlit as st

if st.session_state.img:
    st.image(st.session_state.img)

@st.dialog("Cast your vote")
def vote():
    picture = st.camera_input("Take a picture", disabled=not enable)
    if picture:
        st.session_state.img = picture
        st.rerun()


if st.button("take image"):
    vote()