import streamlit as st # type: ignore
import requests # type: ignore
import json
import os
import pandas as pd
from dotenv import load_dotenv # type: ignore
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate
from connection import contract, w3
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")


def upload_to_pinata(file_path, api_key, api_secret):
    # Set up the Pinata API endpoint and headers
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    # Prepare the file for upload
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}

        # Make the request to Pinata
        response = requests.post(pinata_api_url, headers=headers, files=files)

        # Parse the response
        result = json.loads(response.text)

        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None


options = ("Générer un diplome", "Vérifier les diplomes")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    form = st.form("Generate-Certificate")
    uid = form.text_input(label="ID Etudiant")
    candidate_name = form.text_input(label="Noms")
    course_name = form.text_input(label="Module")
    org_name = form.text_input(label="Université")

    submit = form.form_submit_button("Enregistrer")
    if submit:
        pdf_file_path = "Diplome.pdf"
        institute_logo_path = "../assets/logo.jpg"
        generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)

        # Upload the PDF to Pinata
        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        print(f"IPFS Hash Type: {type(ipfs_hash)}, Value: {ipfs_hash}")
        os.remove(pdf_file_path)
        data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()



        if isinstance(ipfs_hash, dict) and 'IpfsHash' in ipfs_hash:
            ipfs_hash = ipfs_hash['IpfsHash']



        assert isinstance(certificate_id, str)
        assert isinstance(uid, str)
        assert isinstance(candidate_name, str)
        assert isinstance(course_name, str)
        assert isinstance(org_name, str)
        assert isinstance(ipfs_hash, str)
        


        print(type(certificate_id), type(uid), type(candidate_name), type(course_name), type(org_name), type(ipfs_hash))


        # Smart Contract Call
        contract.functions.generateCertificate(certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash).transact({'from': w3.eth.accounts[0]})
        st.success(f"Diplome généré avec succès avec l'ID de diplome : {certificate_id}")

else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Entrez le Diplome ID")
    submit = form.form_submit_button("Soumettre")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Diplome non valide !")







# Fonction pour afficher les certificats
def display_certificates():
    # Lire les données du fichier CSV
    df = pd.read_csv('certificates.csv')

    # Afficher le tableau dans Streamlit
    st.write("Tous les diplômes générés :")
    st.dataframe(df)






# Fonction pour importer un fichier Excel et créer des certificats
def import_and_generate_certificates():
    st.header("Importer un fichier Excel pour générer des certificats")

    uploaded_file = st.file_uploader("Téléchargez un fichier Excel", type=["xlsx"])
    
    if uploaded_file is not None:
        # Lire le fichier Excel
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # Vérifier que le fichier contient les colonnes nécessaires
        required_columns = ["UID", "Nom", "Cours", "Organisation", "LogoInstitut"]
        if all(col in df.columns for col in required_columns):
            st.success("Le fichier a été chargé avec succès !")

            # Parcourir chaque ligne et générer un certificat
            for index, row in df.iterrows():
                uid = row["UID"]
                candidate_name = row["Nom"]
                course_name = row["Cours"]
                org_name = row["Organisation"]
                institute_logo_path = row["LogoInstitut"]  # Chemin relatif du logo (doit être accessible)

                # Avant de générer le certificat
                output_dir = "certificates"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)  # Crée le répertoire s'il n'existe pas

                # Génération du chemin complet
                output_path = os.path.join(output_dir, f"{candidate_name.replace(' ', '_')}_{uid}.pdf")
                generate_certificate(output_path, uid, candidate_name, course_name, org_name, institute_logo_path)
            
            st.success("Les certificats ont été générés avec succès !")
        else:
            st.error(f"Le fichier doit contenir les colonnes suivantes : {', '.join(required_columns)}")










# Appeler la fonction dans l'application Streamlit
if __name__ == "__main__":
    import_and_generate_certificates()
    display_certificates()