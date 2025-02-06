import streamlit as st
from webdav import WebDAVClient
import hashlib
from authentification import login, logout



st.config.set_option("client.showSidebarNavigation", False)
if "has_rerun" not in st.session_state:
    st.session_state.has_rerun = True
    st.rerun()



# Get the list of files in the root directory.
st.warning("INFORMATION D'UTILISATION DES DONNÉES ETC... \n Please do not refresh the pages as if will reset the application.")
st.write("Votre email address ne sera pas enregistrée, mais sera utilisée pour vous identifier.")

understood = st.checkbox("J'ai lu et compris ...", value=False)


if understood:
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        login("Login", "pages/formulaire_sd.py")
    with col2:
        if "current_user" in st.session_state.keys() and st.session_state["current_user"] is not None:
            logout("Logout", "app.py")
        else:
            if st.button("Register"):
                st.session_state.target_page = "pages/formulaire_sd.py"
                st.switch_page("pages/register.py")






