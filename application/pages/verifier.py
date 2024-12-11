import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate
from connection import contract
from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


options = ("Verifier le Diplome en utilisant un PDF", "Voir/Verifier Diplome en utilisant le Diplome ID")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    uploaded_file = st.file_uploader("Téléverser la version PDF de votre Diplome")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("Diplome.pdf", "wb") as file:
            file.write(bytes_data)
        try:
            (uid, candidate_name, course_name, org_name) = extract_certificate("Diplome.pdf")
            displayPDF("Diplome.pdf")
            os.remove("Diplome.pdf")

            # Calculating hash
            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            # Smart Contract Call
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Diplome validé avec succès !")
            else:
                st.error("Diplome non valide ! Le diplome est peut-être falsifié")
        except Exception as e:
            st.error("Diplome non valide ! Le diplome est peut-être falsifié")

elif selected == options[1]:
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Entrez votre Diplome ID")
    submit = form.form_submit_button("Valider")
    if submit:
        try:
            view_certificate(certificate_id)
            # Smart Contract Call
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Diplome authentique!")
            else:
                st.error("Diplome invalide!")
        except Exception as e:
            st.error("Diplome invalide!")