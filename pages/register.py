import streamlit as st
from authentification import login, register

if "current_user" in st.session_state.keys() and st.session_state["current_user"] is not None:
	register("Register", st.session_state["target_page"] if "target_page" in st.session_state.keys() and st.session_state["target_page"] is not None else "app.py")
else:
	st.session_state.current_user = None
	register("Register", st.session_state["target_page"] if "target_page" in st.session_state.keys() and st.session_state["target_page"] is not None else "app.py")


