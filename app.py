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

col1, col2 = st.columns(2)
username = st.text_input("Addresse email", key="USERNAME")
st.write("Votre email address ne sera pas enregistrée, mais sera utilisée pour vous identifier.")

if username:
    m = hashlib.sha256()
    m.update(username.encode())
    st.session_state["CURRENT_USER"] = m.hexdigest()
    if not st.session_state["CURRENT_USER"] in data.keys():
        # Create new user entry
        data[st.session_state["CURRENT_USER"]] = {}
        st.session_state["data"] = data
        stop = False
    elif st.session_state["CURRENT_USER"] in data.keys() and "is_completed" in data.keys() and data[st.session_state["CURRENT_USER"]]["is_completed"]:
        stop = True
    else:
        data[st.session_state["CURRENT_USER"]] = {}
        st.session_state["data"] = data
        stop = False
else:
    stop = True 



st.write(f"Hello {st.session_state['CURRENT_USER']}!" if "CURRENT_USER" in st.session_state.keys() else "Hello!")

col1, col2 = st.columns(2)
with col1:
    # Button resume form
    if st.button("Reprendre le questionnaire"):
        if st.session_state["CURRENT_USER"] in data.keys():
            if "is_completed" not in data[st.session_state["CURRENT_USER"]].keys():
                data[st.session_state["CURRENT_USER"]]["is_completed"] = False
                client.put_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['CURRENT_USER']}.json", data)
                st.switch_page("pages/formulaire_sd.py")
            elif data[st.session_state["CURRENT_USER"]]["is_completed"]:
                st.error("Le questionnaire a déjà été complété et ne peut plus être modifié.")
            else:
                st.switch_page("pages/formulaire_sd.py")
        else:
            st.error("Un utilisateur avec cette addresse email n'existe pas. Veuillez en créer un nouveau.")
with col2:
    # Button new form
    if st.button("Nouveau questionnaire"):
        if st.session_state["CURRENT_USER"] in data.keys():
            st.error("Un utilisateur avec cette addresse existe déjà.")
        else:
            data[st.session_state["CURRENT_USER"]] = {}
            data[st.session_state["CURRENT_USER"]]["is_completed"] = False
            client.put_json(st.secrets["webdav"]["remote_path"] + f"{st.session_state['CURRENT_USER']}.json", data)
            st.switch_page("pages/formulaire_sd.py")

