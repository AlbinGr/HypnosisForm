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
        login("Login", "pages/hypnose_expert.py")
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

if "hypnose_praticien" not in data.keys():
    st.switch_page("pages/formulaire_sd.py")
elif data["hypnose_praticien"] == "Non":
    st.switch_page("pages/audiopage.py")

# Form fields
st.title("En tant qu'hypnothérapeute:")

data["experience_hypnotherapie_expert"] = st.text_input(
    "Depuis combien de temps pratiquez-vous l'hypnose en tant qu'hypnothérapeute ?",
    key="experience_hypnotherapie_expert_expert",
    value = data.get("experience_hypnotherapie_expert", None)
)

data["diplome_principal"] = st.text_input("Dans le cadre de quelle pratique (para)médicale pratiquez-vous l'hypnothérapie (ex. psychothérapie, anesthésie) ?",
    # "Quel est votre diplôme principal dans le domaine médical ou paramédical ?",
    key="diplome_principal", 
    value = data.get("diplome_principal", None)
)

formation_hypnose = st.radio(
    "Avez-vous eu une formation en lien avec l’hypnose ?", 
    ["Oui", "Non"],
    index=["Oui", "Non"].index(data.get("formation_hypnose", "Non")) if data.get("formation_hypnose", None) is not None else None,
    key="formation_hypnose", 
)
data["formation_hypnose"] = formation_hypnose
if formation_hypnose == "Oui":
    data["details_formation_hypnose"] = st.text_input(
        "Si oui, indiquez l’intitulé de cette formation/certification ainsi que l'année d'obtention ?",
        key="details_formation_hypnose", 
        value = data.get("details_formation_hypnose", None)
    )




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
            st.switch_page("pages/audiopage.py")

with col1:
    if st.button("Retour"):
        st.switch_page("pages/hypnose_patient.py")
        
