import streamlit as st
from webdav import WebDAVClient
import hashlib

if "client" not in st.session_state.keys():
	client = WebDAVClient(
		base_url= st.secrets["webdav"]["url"],
		username= st.secrets["webdav"]["email"],
		password= st.secrets["webdav"]["psw"]
	)
	st.session_state["client"] = client
else:
	client = st.session_state["client"]

if "CURRENT_USER" not in st.session_state.keys():
	username = st.text_input("Nom d'utilisateur", key="USERNAME")
	if username:
		m = hashlib.sha256()
		m.update(username.encode())
		username = m.hexdigest()

		# Check if the user exists
		if not client.file_exists(st.secrets["webdav"]["remote_path"] + f"{username}.json"):
			st.error("Nom d'utilisateur inconnu. Retournez à la page d'accueil pour en créer un nouveau si besoin.")
			if st.button("Retour"):
				st.switch_page("app.py")
			st.stop()
		else:
			st.session_state["CURRENT_USER"] = username
			st.rerun()
	else:
		if st.button("Retour"):
			st.switch_page("app.py")
		st.stop()

if "data" not in st.session_state.keys():
	data = client.get_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['CURRENT_USER']}.json")
	st.session_state["data"] = data
else:
	data = st.session_state["data"]

st.title("Questionnaire socio-démographique")

data[st.session_state["CURRENT_USER"]]["age"] = st.number_input(
	"Quel est votre âge ?", 
	min_value=0, 
	max_value=120, 
	step=1, 
	value=data[st.session_state["CURRENT_USER"]].get("age", 0),
	key="age"
)

data[st.session_state["CURRENT_USER"]]["genre"] = st.selectbox(
	"Quel est votre genre ?", 
	["Féminin", "Masculin", "Autre"], 
	index=["Féminin", "Masculin", "Autre"].index(data[st.session_state["CURRENT_USER"]].get("genre", "Féminin")),
	key="genre"
)

data[st.session_state["CURRENT_USER"]]["langue_maternelle"] = st.text_input(
	"Quel est votre langue maternelle ?", 
	value=data[st.session_state["CURRENT_USER"]].get("langue_maternelle", ""),
	key="langue_maternelle"
)

parlez_autres_langues = st.radio(
	"Parlez-vous d'autres langues ?", 
	["Oui", "Non"], 
	index=["Oui", "Non"].index("Oui" if "autres_langues" in data[st.session_state["CURRENT_USER"]] else "Non"),
	key="parlez_autres_langues"
)
if parlez_autres_langues == "Oui":
	data[st.session_state["CURRENT_USER"]]["autres_langues"] = st.text_input(
		"Si oui, lesquelles ?", 
		value=data[st.session_state["CURRENT_USER"]].get("autres_langues", ""),
		key="autres_langues"
	)

st.subheader("Temps d'écoute de la musique")
data[st.session_state["CURRENT_USER"]]["temps_actif"] = st.number_input(
	"En moyenne, combien de temps par jour passez-vous à écouter de la musique de manière active (en minutes) ?", 
	min_value=0, 
	step=1, 
	value=data[st.session_state["CURRENT_USER"]].get("temps_actif", 0),
	key="temps_actif"
)
data[st.session_state["CURRENT_USER"]]["temps_passif"] = st.number_input(
	"En moyenne, combien de temps par jour passez-vous à écouter de la musique de manière passive (en minutes) ?", 
	min_value=0, 
	step=1, 
	value=data[st.session_state["CURRENT_USER"]].get("temps_passif", 0),
	key="temps_passif"
)

pratique_musique = st.selectbox(
	"Pratiquez-vous actuellement un instrument de musique et/ou du chant ?", 
	["Oui, régulièrement", "Oui mais occasionnellement", "Non"], 
	index=["Oui, régulièrement", "Oui mais occasionnellement", "Non"].index(data[st.session_state["CURRENT_USER"]].get("pratique_musique", "Non")),
	key="pratique_musique"
)
data[st.session_state["CURRENT_USER"]]["pratique_musique"] = pratique_musique

problèmes_auditifs = st.radio(
	"Avez-vous déjà présenté des problèmes auditifs ?", 
	["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("problèmes_auditifs", "Non")),
	key="problèmes_auditifs"
)
data[st.session_state["CURRENT_USER"]]["problèmes_auditifs"] = problèmes_auditifs
if problèmes_auditifs == "Oui":
	data[st.session_state["CURRENT_USER"]]["détails_problèmes_auditifs"] = st.text_input(
		"Si oui, lesquels ?", 
		value=data[st.session_state["CURRENT_USER"]].get("détails_problèmes_auditifs", ""),
		key="détails_problèmes_auditifs"
	)

hypnose_patient = st.radio(
	"Êtes-vous familier à l’hypnose en tant que patient ou sujet ?", 
	["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("hypnose_patient", "Non")),
	key="hypnose_patient"
)
data[st.session_state["CURRENT_USER"]]["hypnose_patient"] = hypnose_patient
if hypnose_patient == "Oui":
	data[st.session_state["CURRENT_USER"]]["fréquence_hypnose_patient"] = st.text_input(
		"Si oui, à quelle fréquence ?", 
		value=data[st.session_state["CURRENT_USER"]].get("fréquence_hypnose_patient", ""),
		key="fréquence_hypnose_patient"
	)

hypnose_praticien = st.radio(
	"Êtes-vous familier à l’hypnose en tant que praticien ou thérapeute ?", 
	["Oui", "Non"], 
	index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("hypnose_praticien", "Non")),
	key="hypnose_praticien"
)
data[st.session_state["CURRENT_USER"]]["hypnose_praticien"] = hypnose_praticien
if hypnose_praticien == "Oui":
	data[st.session_state["CURRENT_USER"]]["fréquence_hypnose_praticien"] = st.text_input(
		"Si oui, à quelle fréquence ?", 
		value=data[st.session_state["CURRENT_USER"]].get("fréquence_hypnose_praticien", ""),
		key="fréquence_hypnose_praticien"
	)

st.session_state["data"] = data

col1, col2 = st.columns(2)
# Continue and return button, saving the data to server
with col2:
	if st.button("Continuer"):
		# Save the data to the server
		client.put_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['CURRENT_USER']}.json" , data)
		st.switch_page("pages/hypnose_patient.py")
with col1:
	if st.button("Retour"):
		st.switch_page("app.py")


