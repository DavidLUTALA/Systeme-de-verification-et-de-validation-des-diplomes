import streamlit as st
from db.firebase_app import register
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

form = st.form("login")
email = form.text_input("Entrez votre email")
password = form.text_input("Entrez votre mot de passe", type="password")
clicked_login = st.button("Déjà inscrit ? Cliquez ici pour vous connecter !")

if clicked_login:
    switch_page("login")
    
submit = form.form_submit_button("S'inscrire")
if submit:
    result = register(email, password)
    if result == "success":
        st.success("Registration successful!")
        if st.session_state.profile == "Institute":
            switch_page("institute")
        else:
            switch_page("verifier")
    else:
        st.error("Inscription échouée !")