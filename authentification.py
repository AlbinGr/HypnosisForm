import streamlit as st
from webdav import WebDAVClient
import hashlib
from time import sleep

def login(button_name="Se connecter", target_page = "app.py"):
	email = st.text_input("Nom d'utilisateur")
	password = st.text_input("Mot de passe", type="password")

	hashed_email = hashlib.sha256(email.encode()).hexdigest()
	hashed_password = hashlib.sha256(password.encode()).hexdigest()

	if "client" not in st.session_state.keys():
		client = WebDAVClient(
			base_url= st.secrets["webdav"]["url"],
			username= st.secrets["webdav"]["email"],
			password= st.secrets["webdav"]["psw"]
		)
		st.session_state["client"] = client
	else:
		client = st.session_state["client"]
	

	if st.button(button_name):
		# Add your authentication logic here
		# Check if the user exists and if the password matches
		if client.file_exists(st.secrets["webdav"]["remote_path"] + f"{hashed_email}.json"):
			user_data = client.get_json(st.secrets["webdav"]["remote_path"] + f"{hashed_email}.json")
			if user_data["password"] == hashed_password:
				st.session_state.current_user = hashed_email
				st.switch_page(target_page)
			else:
				st.error("Nom d'utilisateur et mot de passe invalide, veuillez réessayer ou créez un compte en cliquant sur le bouton 'S'enregistrer'")
				sleep(2)
		else:
			st.error("Nom d'utilisateur et mot de passe invalide, veuillez réessayer ou créez un compte en cliquant sur le bouton 'S'enregistrer'")
			sleep(2)

def register(button_name="S'enregistrer", target_page = "app.py"):
	email = st.text_input("Nom d'utilisateur")
	password = st.text_input("Mot de passe", type="password")
	confirmpassword = st.text_input("Confirmez le mot de passe", type="password")

	hashed_email = hashlib.sha256(email.encode()).hexdigest()
	hashed_password = hashlib.sha256(password.encode()).hexdigest()	
	hashed_confirmpassword = hashlib.sha256(confirmpassword.encode()).hexdigest()

	if hashed_password != hashed_confirmpassword:
		st.error("Les mots de passe ne correspondent pas")
		st.stop()

	if "client" not in st.session_state.keys():
		client = WebDAVClient(
			base_url= st.secrets["webdav"]["url"],
			username= st.secrets["webdav"]["email"],
			password= st.secrets["webdav"]["psw"]
		)
		st.session_state["client"] = client	
	else:
		client = st.session_state["client"]

	if st.button(button_name):
		# Add your registration logic here
		# Check if the user exists and if the password matches
		if client.file_exists(st.secrets["webdav"]["remote_path"] + f"{hashed_email}.json"):
			st.error("Utilisateur déjà existant")
			sleep(2)
		else:
			client.put_json(st.secrets["webdav"]["remote_path"] + f"{hashed_email}.json", {"password": hashed_password})
			st.session_state.current_user = hashed_email
			st.switch_page(target_page)

def logout(button_name="Déconnection", target_page = "app.py"):
	if st.button(button_name):
		st.session_state.current_user = None
		st.switch_page(target_page)



