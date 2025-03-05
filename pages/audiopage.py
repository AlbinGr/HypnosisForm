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
        login("Login", "pages/audiopage.py")
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

st.title("Évaluation d'écoute")

st.header("Pour information :")
st.write("L’état de transe hypnotique est un état modifié de conscience caractérisé par :")
st.write("    - une focalisation intense sur une idée ou une sensation")
st.write("    - une diminution de la perception de l’environnement extérieur")
st.write("    - une ouverture accrue aux suggestions.")
st.write("Ce n’est pas une perte de contrôle ou de conscience, mais un état dans lequel on peut ressentir une relaxation profonde, \
         une distorsion du temps, ou une concentration très spécifique.")
st.header("Consigne")
st.write(
	"""Vous allez écouter successivement des enregistrements de maximum 1 minute. Nous ne vous demandons pas de vous focaliser sur le contenu (le sens des mots et / ou des phrases)
        mais bien sur la façon dont est délivré ce contenu (la voix, la parole). Sur une échelle de 1 à 10, vous indiquerez dans quelle mesure l'enregistrement est susceptible 
        d'induire un état de transe.""")

st.header("Qualité d'écoute")
st.write(""" Avant de commencer l'expérience, veuillez vous munir d'une casque ou d'écouteurs. Vérifiez que le volume est réglé de manière confortable sur votre appareil (téléphone, tablette, ordinateur) de sorte que vous puissiez entendre clairement, sans gêne. Si le son est trop faible ou trop fort, ajustez le volume en conséquence, en gardant une intensité agréable. Une fois le volume réglé, veillez à ne pas le modifier tout au long de l'expérience. Pour tester le volume de votre appareil, cliquez ici :""")

if st.button("Commencer l'évaluation"):
    st.switch_page("pages/evalpage.py")
# TODO Make this page better (with return etc...)

