import re
import streamlit as st
st.set_page_config(page_title="Hospital Management & Chatbot", layout="wide")
import datetime

# Mock database (in-memory)
patients = []
def chatbot_response(user_input):
    user_input = user_input.lower()
    # Appointment queries
    if re.search(r"\b(appointment|book|schedule|register)\b", user_input):
        return "You can book an appointment under the 'Patient Registration' section."
    # Hospital timings queries
    elif re.search(r"\b(time|timing|hours|open|close|working)\b", user_input):
        return "Our hospital operates from 8 AM to 8 PM, Monday to Saturday."
    # Emergency queries
    elif re.search(r"\b(emergency|urgent|help|accident|ambulance)\b", user_input):
        return "For emergencies, please call our 24/7 helpline: 1800-000-911."
    # Patient info queries
    elif re.search(r"\b(patient|registered|list|show)\b", user_input):
        if patients:
            return f"We currently have {len(patients)} registered patients."
        else:
            return "No patients are registered yet."
    else:
        return "I'm sorry, I didn't understand that. You can ask about appointments, hospital hours, emergency services, or registered patients."

# Streamlit App


st.title("🏥 Hospital Management System with 🤖 Chatbot")

# Two-column layout
col1, col2 = st.columns(2)

# --- Column 1: Hospital Management ---
with col1:
    st.header("📋 Patient Registration")

    with st.form("patient_form"):
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        symptoms = st.text_area("Symptoms")
        appointment_date = st.date_input("Preferred Appointment Date", datetime.date.today())
        submit = st.form_submit_button("Register")

        if submit:
            patient = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Symptoms": symptoms,
                "Appointment Date": appointment_date
            }
            patients.append(patient)
            st.success(f"✅ {name} registered successfully!")

    st.subheader("🧾 Registered Patients")
    if patients:
        st.table(patients)
    else:
        st.info("No patients registered yet.")

# --- Column 2: Chatbot ---
with col2:
    st.header("🤖 Hospital Assistant Chatbot")
    st.write("Ask about appointments, timings, or emergency services.")
    # Initialize chat history in session state

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    user_input = st.text_input("You:", key="user_input")
    if st.button("Send"):
        if user_input.strip() != "":
            response = chatbot_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))

    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 Bot:** {message}")