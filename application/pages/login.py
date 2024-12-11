import streamlit as st
from db.firebase_app import login
from dotenv import load_dotenv
import os
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

form = st.form("login")
email = form.text_input("Entrez votre email")
password = form.text_input("Entrez votre mot de passe", type="password")

if st.session_state.profile != "Institute":
    clicked_register = st.button("Nouvel utilisateur ? Cliquez ici pour vous inscrire !")

    if clicked_register:
        switch_page("register")

submit = form.form_submit_button("Se connecter")
if submit:
    if st.session_state.profile == "Institute":
        valid_email = os.getenv("institute_email")
        valid_pass = os.getenv("institute_password")
        if email == valid_email and password == valid_pass:
            switch_page("institute")
        else:
            st.error("Identifiants incorrects, veuillez vérifier votre email ou mot de passe")
    else:
        result = login(email, password)
        if result == "success":
            st.success("Login successful!")
            switch_page("verifier")
        else:
            st.error("Identifiants incorrects, veuillez vérifier votre email ou mot de passe")
        