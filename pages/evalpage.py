import datetime
import streamlit as st
from webdav import WebDAVClient
from authentification import login, logout
import numpy as np
import copy

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
        login("Login", "pages/evalpage.py")
    with col2:
        if st.button("Return to homepage"):
            st.switch_page("app.py")
    st.stop()

    
logout("Logout", "app.py")

def create_list(client):
    # Get the xlxs file from server
    df = client.get_csv(st.secrets["webdav"]["base_path"] + "Enregistrements_Hypnose_Streamlit.xlsx")
    file_list = []
    file_list_retest = []
    file_list_h = []
    file_list_c = []
    for l in df["Locuteur"].unique():
        # Create a list of audio for each speaker
        df_l = df[df["Locuteur"] == l][["Condition (LC, LH)", "Chemin DoX"]]
        # Take 3 random LH and 1 random LC
        df_l_h = df_l[df_l["Condition (LC, LH)"] == "LH"].sample(3, replace = False)["Chemin DoX"].tolist()
        df_l_c = df_l[df_l["Condition (LC, LH)"] == "LC"].sample(1)["Chemin DoX"].tolist()
        file_list_h.extend(df_l_h)
        file_list_c.extend(df_l_c)

    file_list_c_retest = np.random.choice(copy.deepcopy(file_list_c), 6, replace = False)
    file_list_h_retest = np.random.choice(copy.deepcopy(file_list_h), 19, replace = False)

    file_list.extend(file_list_c)
    file_list.extend(file_list_h)

    file_list_retest.extend(file_list_c_retest)
    file_list_retest.extend(file_list_h_retest)
    # Random mixe the list
    np.random.shuffle(file_list)
    np.random.shuffle(file_list_retest)

    return file_list + file_list_retest


if "data" not in st.session_state.keys() or st.session_state["data"] is None:
    data = st.session_state["client"].get_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['current_user']}.json")
    st.session_state["data"] = data
else:
    data = st.session_state["data"]

# If list of audio is not in data or None, create it
if "audio_list" not in data.keys() or data["audio_list"] is None:
    data["audio_list"] = create_list(client)
    data["results"] = []
    st.session_state["data"] = data

if "current_audio_path" not in st.session_state.keys():
    st.session_state["current_audio_path"] = st.session_state["data"]["audio_list"][0] if len(st.session_state["data"]["audio_list"]) > 0 else None
if "current_audio" not in st.session_state.keys():
    st.session_state["current_audio"] = client.get_audio(st.session_state["current_audio_path"]) if st.session_state["current_audio_path"] is not None else None

st.write(f"Il vous reste {len(st.session_state['data']['audio_list'])} enregistrements à évaluer.")

col1, col2 = st.columns(2, vertical_alignment="bottom")
with col1:
    if st.button("Etat de transe hypnotique"):
        if "button_trance_text" not in st.session_state.keys() or st.session_state["button_trance_text"] == False:
            st.session_state["button_trance_text"] = True
        else:
            st.session_state["button_trance_text"] = False
with col2:
    if st.button("Consignes"):
        if "button_consignes_text" not in st.session_state.keys() or st.session_state["button_consignes_text"] == False:
            st.session_state["button_consignes_text"] = True
        else:
            st.session_state["button_consignes_text"] = False

if "button_trance_text" in st.session_state.keys() and st.session_state["button_trance_text"]:
    st.write("L’état de transe hypnotique est un état modifié de conscience caractérisé par :")
    st.write("    - une focalisation intense sur une idée ou une sensation")
    st.write("    - une diminution de la perception de l’environnement extérieur")
    st.write("    - une ouverture accrue aux suggestions.")
    st.write("Ce n’est pas une perte de contrôle ou de conscience, mais un état dans lequel on peut ressentir une relaxation profonde, \
            une distorsion du temps, ou une concentration très spécifique.")
    
if "button_consignes_text" in st.session_state.keys() and st.session_state["button_consignes_text"]:
    st.write(
	"""Vous allez écouter successivement des enregistrements de maximum 1 minute. Nous ne vous demandons pas de vous focaliser sur le contenu (le sens des mots et / ou des phrases)
        mais bien sur la façon dont est délivré ce contenu (la voix, la parole). Sur une échelle de 1 (pas du tout) à 10 (tout à fait), vous indiquerez dans quelle mesure l'enregistrement est susceptible 
        d'induire un état de transe.""")

            

if st.session_state["current_audio"] is not None:
    st.audio(st.session_state["current_audio"][0], autoplay=True, sample_rate=st.session_state["current_audio"][1]) 
else:
    st.switch_page("pages/lastpage.py")

options = ["1 (Pas du tout d'accord)", "2", "3", "4", "5", "6", "7", "8", "9", "10 (Tout à fait d'accord)"]
result = st.select_slider("Dans quelle mesure cet enregistrement est-il susceptible d'induire l'état de transe hypnotique ?",\
                          options= options, key="hypnotique", value = None)


if st.button("Suivant"):
    # Save the result in the data
    st.session_state["data"]["results"].append([st.session_state["current_audio_path"], result, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    # Remove the current audio from the list
    st.session_state["data"]["audio_list"] = list(st.session_state["data"]["audio_list"][1:])
    # Save the data to server
    st.session_state["client"].put_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['current_user']}.json", st.session_state["data"])
    # If there is more audio, get the next one
    del st.session_state["current_audio_path"]
    del st.session_state["current_audio"]
    
    if len(st.session_state["data"]["audio_list"]) > 0:
        st.switch_page("pages/evalpage.py")
    else:
        st.switch_page("pages/lastpage.py")
