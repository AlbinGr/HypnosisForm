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

if "data" not in st.session_state.keys():
	data = client.get_json(st.secrets["webdav"]["remote_path"])
	st.session_state["data"] = data
else:
	data = st.session_state["data"]

if "CURRENT_USER" not in st.session_state.keys():
	username = st.text_input("Nom d'utilisateur", key="USERNAME")
	if username:
		m = hashlib.sha256()
		m.update(username.encode())
		username = m.hexdigest()
		if not username in data.keys():
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
    
if "hypnose_praticien" in data[st.session_state["CURRENT_USER"]].keys():
    st.switch_page("pages/formulaire_sd.py")
elif data[st.session_state["CURRENT_USER"]]["hypnose_praticien"] == "Non":
    st.switch_page("pages/kappa1.py")

# Form fields
st.title("Formulaire SD expert")

data[st.session_state["CURRENT_USER"]]["experience_hypnotherapie"] = st.text_input(
    "Depuis combien de temps pratiquez-vous l'hypnothérapie ?",
    value=data[st.session_state["CURRENT_USER"]].get("experience_hypnotherapie", "")
)

data[st.session_state["CURRENT_USER"]]["diplome_principal"] = st.text_input(
    "Quel est votre diplôme principal dans le domaine médical ou paramédical ?",
    value=data[st.session_state["CURRENT_USER"]].get("diplome_principal", "")
)

formation_hypnose = st.radio(
    "Avez-vous eu une formation en lien avec l’hypnose ?", 
    ["Oui", "Non"],
    index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("formation_hypnose", "Non"))
)
data[st.session_state["CURRENT_USER"]]["formation_hypnose"] = formation_hypnose
if formation_hypnose == "Oui":
    data[st.session_state["CURRENT_USER"]]["details_formation_hypnose"] = st.text_input(
        "Si oui, la ou lesquelles ? En quelle année l'avez-vous réalisée ?",
        value=data[st.session_state["CURRENT_USER"]].get("details_formation_hypnose", "")
    )

connaissance_relaxation = st.radio(
    "Avez-vous des connaissances ou une expérience particulière dans d'autres techniques de relaxation ou de méditation ?",
    ["Oui", "Non"],
    index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("connaissance_relaxation", "Non"))
)
data[st.session_state["CURRENT_USER"]]["connaissance_relaxation"] = connaissance_relaxation
if connaissance_relaxation == "Oui":
    data[st.session_state["CURRENT_USER"]]["details_relaxation"] = st.text_input(
        "Si oui, pourriez-vous préciser ?",
        value=data[st.session_state["CURRENT_USER"]].get("details_relaxation", "")
    )

experience_transe = st.radio(
    "Avez-vous déjà eu des expériences personnelles liées à la transe hypnotique (détente profonde, altération de la perception du temps, etc.) ?",
    ["Oui", "Non"],
    index=["Oui", "Non"].index(data[st.session_state["CURRENT_USER"]].get("experience_transe", "Non"))
)
data[st.session_state["CURRENT_USER"]]["experience_transe"] = experience_transe
if experience_transe == "Oui":
    data[st.session_state["CURRENT_USER"]]["details_transe"] = st.text_area(
        "Si oui, pouvez-vous brièvement décrire cette expérience ?",
        value=data[st.session_state["CURRENT_USER"]].get("details_transe", "")
    )


st.session_state["data"] = data

# Submit button
col1, col2 = st.columns(2)

with col2:
    if st.button("Continuer"):
        client.put_json(st.secrets["webdav"]["remote_path"], data)
        st.switch_page("pages/kappa1.py")

with col1:
    if st.button("Retour"):
        if data[st.session_state["CURRENT_USER"]]["hypnose_patient"] == "Oui":
            st.switch_page("pages/hypnose_patient.py")
        else:
            st.switch_page("pages/formulaire_sd.py")
