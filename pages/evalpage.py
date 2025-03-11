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
    for h in df["Locuteur"].unique():
        # Create a list of audio for each speaker
        df_h = df[df["Locuteur"] == h][["Condition (LC, LH)", "Chemin DoX"]]
        # Take 3 random LH and 1 random LC
        df_h = df_h[df_h["Condition (LC, LH)"] == "LH"].sample(3, replace = False)["Chemin DoX"].tolist() +\
                        df_h[df_h["Condition (LC, LH)"] == "LC"].sample(1)["Chemin DoX"].tolist()

        file_list.extend(df_h)

    # 20 % retest
    retake_list = np.random.choice(file_list, int(0.2*len(file_list)), replace = False)
    file_list.extend(retake_list)
    # Save the list to the server
    client.put_json(st.secrets["webdav"]["base_path"] + f"{h}.json", {"audio_list": file_list, "results": []})

    return list(file_list) 


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

if st.session_state["current_audio"] is not None:
    st.audio(st.session_state["current_audio"][0], autoplay=True, sample_rate=st.session_state["current_audio"][1]) 
else:
    st.switch_page("pages/lastpage.py")

options = ["Pas du tout d'accord", "Plutôt pas d'accord", "Neutre", "Plutôt d'accord", "Tout à fait d'accord"]
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
