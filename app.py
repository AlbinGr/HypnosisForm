import streamlit as st
from datetime import date

st.title("Form")

# Name Input
st.header("Name")
first_name = st.text_input("First Name", placeholder="Enter your first name")
last_name = st.text_input("Last Name", placeholder="Enter your last name")

# Email Input
st.header("Email")
email = st.text_input("Email", placeholder="example@example.com")

# Address Input
st.header("Address")
street_address = st.text_input("Street Address", placeholder="Enter your street address")
address_line_2 = st.text_input("Street Address Line 2 (Optional)", placeholder="Apartment, suite, etc.")
city = st.text_input("City", placeholder="Enter your city")
state = st.text_input("State/Province", placeholder="Enter your state or province")
postal_code = st.text_input("Postal/Zip Code", placeholder="Enter your postal or zip code")

# Rating Questions
st.header("Questions")
question_1 = st.radio("Type a question (1)", options=[1, 2, 3, 4, 5], horizontal=True)
question_2 = st.radio("Type a question (2)", options=[1, 2, 3, 4, 5], horizontal=True)

# Submit Button
if st.button("Submit"):
    st.success("Form submitted successfully!")
    st.write("### Submitted Information")
    st.write(f"**Name:** {first_name} {last_name}")
    st.write(f"**Email:** {email}")
    st.write(f"**Street Address:** {street_address}")
    if address_line_2:
        st.write(f"**Street Address Line 2:** {address_line_2}")
    st.write(f"**City:** {city}")
    st.write(f"**State/Province:** {state}")
    st.write(f"**Postal/Zip Code:** {postal_code}")
    st.write(f"**Question 1 Rating:** {question_1}")
    st.write(f"**Question 2 Rating:** {question_2}")