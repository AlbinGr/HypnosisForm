import streamlit as st
from webdav import WebDAVClient
import hashlib


if "data" not in st.session_state.keys():
    data = {}
    st.session_state["data"] = data
else:
    data = st.session_state["data"]

if "client" not in st.session_state.keys():
	client = WebDAVClient(
		base_url= st.secrets["webdav"]["url"],
		username= st.secrets["webdav"]["email"],
		password= st.secrets["webdav"]["psw"]
		)
	st.session_state["client"] = client
else:
	client = st.session_state["client"]



# TODO : Reload the data given a user unique key/password

st.config.set_option("client.showSidebarNavigation", False)
if "has_rerun" not in st.session_state:
    st.session_state.has_rerun = True
    st.rerun()



# Get the list of files in the root directory.
st.warning("INFORMATION D'UTILISATION DES DONNÉES ETC... \n Please do not refresh the pages as if will reset the application.")

understood = st.checkbox("J'ai lu et compris ...", value=False)
data = {}

username = st.text_input("Nom d'utilisateur", key="USERNAME")
if username:
    m = hashlib.sha256()
    m.update(username.encode())
    st.session_state["CURRENT_USER"] = m.hexdigest()
    if not st.session_state["CURRENT_USER"] in data.keys():
        # Create new user entry
        data[st.session_state["CURRENT_USER"]] = {}
        client.put_json(st.secrets["webdav"]["remote_path"], data)
        st.session_state["data"] = data
        stop = False
    elif st.session_state["CURRENT_USER"] in data.keys() and "is_completed" in data.keys() and data[st.session_state["CURRENT_USER"]]["is_completed"]:
        stop = True
    else:
        data[st.session_state["CURRENT_USER"]] = {}
        client.put_json(st.secrets["webdav"]["remote_path"], data)
        st.session_state["data"] = data
        stop = False
else:
    stop = True 

st.write(f"Hello {st.session_state['CURRENT_USER']}!" if "CURRENT_USER" in st.session_state.keys() else "Hello!")
         
if st.button("Commencer le questionnaire"):
    if understood and not stop:
        if "is_completed" not in data[st.session_state["CURRENT_USER"]].keys():
            data[st.session_state["CURRENT_USER"]]["is_completed"] = False
            client.put_json(st.secrets["webdav"]["remote_path"], data)

        st.switch_page("pages/formulaire_sd.py")
    elif stop:
        st.error("Un utilisateur avec ce nom existe déjà et a déjà complété le questionnaire.")
    else:
        st.error("Veuillez lire et comprendre les informations d'utilisation des données.")

