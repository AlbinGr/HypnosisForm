import streamlit as st
from webdav import WebDAVClient

if "CURRENT_USER" not in st.session_state.keys():
    st.session_state["CURRENT_USER"] =  st.experimental_user.to_dict()["email"]

    

st.config.set_option("client.showSidebarNavigation", False)
if "has_rerun" not in st.session_state:
    st.session_state.has_rerun = True
    st.rerun()

st.write(f"Hello {st.session_state['CURRENT_USER']}!")

# Create a connection object.
data_client = WebDAVClient(
    base_url= st.secrets["webdav"]["url"],
    username= st.secrets["webdav"]["email"],
    password= st.secrets["webdav"]["psw"]
)



# Get the list of files in the root directory.
st.warning("INFORMATION D'UTILISATION DES DONNÉES ETC...")

understood = st.checkbox("J'ai lu et compris ...", value=False)

if st.button("Commencer le questionnaire"):
    if understood:
        st.switch_page("pages/formulaire_sd.py")
    else:
        st.error("Veuillez lire et comprendre les informations d'utilisation des données.")

