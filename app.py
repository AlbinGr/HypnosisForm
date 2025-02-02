import streamlit as st
from webdav import WebDAVClient
import hashlib

if "CURRENT_USER" not in st.session_state.keys():
    m = hashlib.sha256()
    m.update(st.experimental_user.email.encode())
    st.session_state["CURRENT_USER"] = m.hexdigest()

    

st.config.set_option("client.showSidebarNavigation", False)
if "has_rerun" not in st.session_state:
    st.session_state.has_rerun = True
    st.rerun()

st.write(f"Hello {st.session_state['CURRENT_USER']}!")
st.write("Test")

# Get the list of files in the root directory.
st.warning("INFORMATION D'UTILISATION DES DONNÉES ETC...")

understood = st.checkbox("J'ai lu et compris ...", value=False)

if st.button("Commencer le questionnaire"):
    if understood:
        st.switch_page("pages/formulaire_sd.py")
    else:
        st.error("Veuillez lire et comprendre les informations d'utilisation des données.")

