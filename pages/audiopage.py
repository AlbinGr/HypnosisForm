import streamlit as st

if 'id' not in st.session_state:
    st.write('id not in session state')
else:
    st.write(st.session_state.id)

if st.button('Go back'):
    st.switch_page('app.py')