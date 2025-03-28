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
        login("Login", "pages/formulaire_sd.py")
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



st.title("Informations générales")

data["age"] = st.number_input(
    "Quel est votre âge ?", 
    min_value=0, 
    max_value=120, 
    step=1, 
    key="age", 
    value=data.get("age", None)
)

data["genre"] = st.selectbox(
    "Quel est votre genre ?", 
    ["Selection", "Féminin", "Masculin", "Autre"], 
    key="genre", 
    index=["Selection", "Féminin", "Masculin", "Autre"].index(data.get("genre", "Selection"))
)

data["langue_maternelle"] = st.text_input(
    "Quelle est votre langue maternelle ? ", 
    key="langue_maternelle", 
    value=data.get("langue_maternelle", None)
)

data["parlez_autres_langues"] = st.radio(
    "Parlez-vous d’autres langues ?", 
    ["Oui", "Non"], 
    key="parlez_autres_langues", 
    index=["Oui", "Non"].index(data.get("parlez_autres_langues", None)) if data.get("parlez_autres_langues", None) is not None else None
)
if data["parlez_autres_langues"] == "Oui":
    data["autres_langues"] = st.text_input(
        "Si oui, lesquelles ?", 
        key="autres_langues", 
        value=data.get("autres_langues", "")
    )

st.subheader("Temps d'écoute de la musique")
data["temps_actif"] = st.number_input(
    "En moyenne, combien de minutes par jour passez-vous à écouter de la musique de manière active (par exemple, en prêtant attention à un concert ou à une playlist) ?", 
    min_value=0, 
    step=1, 
    key="temps_actif", 
    value=data.get("temps_actif", None)
)
data["temps_passif"] = st.number_input(
    "En moyenne, combien de minutes par jour passez-vous à écouter de la musique de manière passive (par exemple, lorsque la musique joue en arrière-plan comme à la radio ou dans une autre pièce) ? ", 
    min_value=0, 
    step=1, 
    key="temps_passif", 
    value=data.get("temps_passif", None)
)

data["pratique_musique"] = st.selectbox(
    "Pratiquez-vous actuellement un instrument de musique et/ou du chant ?", 
    ["Selection", "Oui", "Non"], 
    key="pratique_musique",
    index=["Selection", "Oui", "Non"].index(data.get("pratique_musique", "Selection")) 
)
if data["pratique_musique"] == "Oui":
    data["instrument_pratiqué"] = st.number_input(
        "Si oui, quelle est votre durée moyenne de pratique par semaine (en minutes)?", 
        key="instrument_pratiqué", 
        min_value=0,
        max_value = 7*24,
        value=data.get("instrument_pratiqué", 0)
    )

data["problèmes_auditifs"] = st.radio(
    "Avez-vous déjà présenté des problèmes auditifs ?", 
    ["Oui", "Non"], 
    key="problèmes_auditifs", 
    index=["Oui", "Non"].index(data.get("problèmes_auditifs", None)) if data.get("problèmes_auditifs", None) is not None else None
)
if data["problèmes_auditifs"] == "Oui":
    data["détails_problèmes_auditifs"] = st.text_input(
        "Si oui, lesquels ?", 
        key="détails_problèmes_auditifs", 
        value=data.get("détails_problèmes_auditifs", "")
    )

hypnose_familiarity = st.radio("Êtes-vous familier avec l’hypnose ?", 
    ["Oui", "Non"], 
    key="hypnose_familiarity", 
    index=["Oui", "Non"].index(data.get("hypnose_familiarity", None)) if data.get("hypnose_familiarity", None) is not None else None
)
data["hypnose_familiarity"] = hypnose_familiarity
if hypnose_familiarity == "Oui":
    hypnose_patient = st.radio(
        "Êtes-vous familier à l’hypnose en tant que patient ou sujet ?", 
        ["Oui", "Non"], 
        key="hypnose_patient", 
        index=["Oui", "Non"].index(data.get("hypnose_patient", None)) if data.get("hypnose_patient", None) is not None else None
    )
    data["hypnose_patient"] = hypnose_patient
    if hypnose_patient == "Oui":
        data["fréquence_hypnose_patient"] = st.text_input(
            "Si oui, combien de séances d'hypnose avez-vous réalisées en tant que patient/sujet ?", 
            key="fréquence_hypnose_patient", 
            value=data.get("fréquence_hypnose_patient", None)
        )

    hypnose_praticien = st.radio(
        "Êtes-vous ou avez-vous été hypnothérapeute dans le domaine (para)médical (ex. psychothérapie, anesthésiologie, etc) ?", 
        ["Oui", "Non"], 
        key="hypnose_praticien", 
        index=["Oui", "Non"].index(data.get("hypnose_praticien", None)) if data.get("hypnose_praticien", None) is not None else None
    )
    data["hypnose_praticien"] = hypnose_praticien
    if hypnose_praticien == "Oui":
        data["fréquence_hypnose_praticien"] = st.text_input(
            "Si oui, à quelle fréquence et pendant combien de temps (ex. tous les jours pendant 5 ans) ?", 
            key="fréquence_hypnose_praticien", 
            value=data.get("fréquence_hypnose_praticien", "")
        )
else: 
    data["hypnose_patient"] = "Non"
    data["hypnose_praticien"] = "Non"

st.session_state["data"] = data

col1, col2 = st.columns(2)
# Continue and return button, saving the data to server
with col2:
    if st.button("Continuer"):
        # Save the data to the server
        # Check if any input is None
        error = False
        for key, value in data.items():
            if value is None or value == "Selection":
                st.error(f"Veuillez remplir le champ: {key}")
                error = True
                break
        if not error:
            st.session_state["client"].put_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['current_user']}.json" , data)
            st.switch_page("pages/hypnose_patient.py")
with col1:
    if st.button("Retour"):
        st.switch_page("app.py")


