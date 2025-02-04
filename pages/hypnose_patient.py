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
	
if "hypnose_patient" not in data[st.session_state["CURRENT_USER"]].keys():
    st.switch_page("pages/formulaire_sd.py")
elif data[st.session_state["CURRENT_USER"]]["hypnose_patient"] == "Non":
    st.switch_page("pages/hypnose_expert.py")

# Form fields
st.title("Formulaire SD patient")

# Set default values if available
default_accord_hypnose_fiable = data.get("accord_hypnose_fiable", 3)
default_accord_hypnose_impact = data.get("accord_hypnose_impact", 3)
default_experience_hypnotherapie = data.get("experience_hypnotherapie", "Je n'ai jamais réalisé de séance d'hypnothérapie")
default_nombre_seances = data.get("nombre_seances", 1)
default_connaissance_relaxation = data.get("connaissance_relaxation", "Non")
default_details_relaxation = data.get("details_relaxation", "")
default_experience_transe = data.get("experience_transe", "Non")
default_details_transe = data.get("details_transe", "")

data["accord_hypnose_fiable"] = st.slider(
    "À quel point êtes-vous d’accord avec l’affirmation suivante : L’hypnose est une pratique fiable et efficace.", 1, 5, default_accord_hypnose_fiable, key="accord_hypnose_fiable")

data["accord_hypnose_impact"] = st.slider(
    "À quel point êtes-vous d’accord avec l’affirmation suivante : Je crois que l’hypnose peut avoir un impact positif sur moi.", 1, 5, default_accord_hypnose_impact, key="accord_hypnose_impact")

experience_hypnotherapie = st.radio(
    "Quelle est votre expérience en hypnothérapie ?",
    ["Je n'ai jamais réalisé de séance d'hypnothérapie", "J'ai déjà participé à une ou des séance(s) d'hypnothérapie"],
    index=["Je n'ai jamais réalisé de séance d'hypnothérapie", "J'ai déjà participé à une ou des séance(s) d'hypnothérapie"].index(default_experience_hypnotherapie),
    key="experience_hypnotherapie"
)
data["experience_hypnotherapie"] = experience_hypnotherapie

if experience_hypnotherapie == "J'ai déjà participé à une ou des séance(s) d'hypnothérapie":
    data["nombre_seances"] = st.number_input(
        "Si vous en avez déjà réalisé des séances, combien en avez-vous eu ?", min_value=1, step=1, value=default_nombre_seances, key="nombre_seances")

connaissance_relaxation = st.radio(
    "Avez-vous des connaissances ou une expérience particulière dans d'autres techniques de relaxation ou de méditation ?",
    ["Oui", "Non"],
    index=["Oui", "Non"].index(default_connaissance_relaxation),
    key="connaissance_relaxation"
)
data["connaissance_relaxation"] = connaissance_relaxation

if connaissance_relaxation == "Oui":
    data["details_relaxation"] = st.text_input("Si oui, pourriez-vous préciser ?", value=default_details_relaxation, key="details_relaxation")

experience_transe = st.radio(
    "Avez-vous déjà eu des expériences personnelles liées à la transe hypnotique (détente profonde, altération de la perception du temps, etc.) ?",
    ["Oui", "Non"],
    index=["Oui", "Non"].index(default_experience_transe),
    key="experience_transe"
)
data["experience_transe"] = experience_transe

if experience_transe == "Oui":
    data["details_transe"] = st.text_area("Si oui, pouvez-vous brièvement décrire cette expérience ?", value=default_details_transe, key="details_transe")

st.session_state["data"] = data
# Submit button

col1, col2 = st.columns(2)

with col2:
    if st.button("Continuer"):
        client.put_json(st.secrets["webdav"]["remote_path"]  + f"{st.session_state['CURRENT_USER']}.json", data)
        st.switch_page("pages/hypnose_expert.py")

with col1:
    if st.button("Retour"):
        st.switch_page("pages/formulaire_sd.py")
