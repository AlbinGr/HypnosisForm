import streamlit as st
from webdav import WebDAVClient
from authentification import login, logout

if "client" not in st.session_state.keys():
    client = WebDAVClient(
        base_url= st.secrets["webdav"]["url"],
        username= st.secrets["webdav"]["email"],
        password= st.secrets["webdav"]["psw"]
    )
    st.session_state["client"] = client
else:
    client = st.session_state["client"]



if "current_user" not in st.session_state.keys() or st.session_state["current_user"] is None:
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        login("Login", "pages/hypnose_patient.py")
    with col2:
        if st.button("Return to homepage"):
            st.switch_page("app.py")
    st.stop()

    
logout("Logout", "app.py")


if "data" not in st.session_state.keys() or st.session_state["data"] is None:
    data = st.session_state["client"].get_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['current_user']}.json")
    st.session_state["data"] = data
else:
    data = st.session_state["data"]
	
if "hypnose_patient" not in data.keys():
    st.switch_page("pages/formulaire_sd.py")

# Form fields
st.title("Formulaire SD patient")

# Set default values if available
default_accord_hypnose_fiable = data.get("accord_hypnose_fiable", None)
default_accord_hypnose_impact = data.get("accord_hypnose_impact", None)
default_experience_hypnotherapie_patient = data.get("experience_hypnotherapie_patient", None)
default_nombre_seances = data.get("nombre_seances", 0)
default_connaissance_relaxation = data.get("connaissance_relaxation", None)
default_details_relaxation = data.get("details_relaxation", "")
default_experience_transe = data.get("experience_transe", None)
default_details_transe = data.get("details_transe", "")

data["accord_hypnose_fiable"] = st.slider(
    "À quel point êtes-vous d’accord avec l’affirmation suivante : L’hypnose est une pratique fiable et efficace. 1 = pas du tout d'accord ; 5 = tout à fait d'accord", 1, 5, default_accord_hypnose_fiable, key="accord_hypnose_fiable")

data["accord_hypnose_impact"] = st.slider(
    "À quel point êtes-vous d’accord avec l’affirmation suivante : Je crois que l’hypnose peut avoir un impact positif sur moi. 1 = pas du tout d'accord ; 5 = tout à fait d'accord", 1, 5, default_accord_hypnose_impact, key="accord_hypnose_impact")


data["experience_hypnotherapie_patient"] = "NA"

data["nombre_seances"] = 0

connaissance_relaxation = st.radio(
    "Avez-vous des connaissances ou une expérience particulière dans d'autres techniques de relaxation ou de méditation ?",
    ["Oui", "Non"],
    index=["Oui", "Non"].index(default_connaissance_relaxation) if default_connaissance_relaxation is not None else None,
    key="connaissance_relaxation"
)
data["connaissance_relaxation"] = connaissance_relaxation

if connaissance_relaxation == "Oui":
    data["details_relaxation"] = st.text_input("Si oui, pourriez-vous préciser ?", value=default_details_relaxation, key="details_relaxation")
else:
    data["details_relaxation"] = ""


st.session_state["data"] = data
# Submit button

col1, col2 = st.columns(2)

with col2:
    if st.button("Continuer"):
        error = False
        for key, value in data.items():
            if value is None or value == "Selection":
                st.error(f"Veuillez remplir le champ: {key}")
                error = True
                break
        if not error:
            st.session_state["client"].put_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['current_user']}.json" , data)
            st.switch_page("pages/hypnose_expert.py")

with col1:
    if st.button("Retour"):
        st.switch_page("pages/formulaire_sd.py")
