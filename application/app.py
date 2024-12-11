import streamlit as st
from PIL import Image
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


st.title("Système de vérification de diplomes")
st.write("")
st.subheader("Selectionner un role")

col1, col2 = st.columns(2)
institite_logo = Image.open("../assets/institute_logo.jpg")
with col1:
    st.image(institite_logo, output_format="jpg", width=230)
    clicked_institute = st.button("Université")

company_logo = Image.open("../assets/company_logo.jpg")
with col2:
    st.image(company_logo, output_format="jpg", width=230)
    clicked_verifier = st.button("Vérificateur")

if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')
