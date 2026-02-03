import streamlit as st
from utils.display import show_dataframe_box
from utils.helpers import format_time
import pandas as pd
import os
def doctor_dashboard(username, doctor_db, appt_db):
    st.title("🩺 Doctor Dashboard")
    menu = st.selectbox("Select Action", [
        "View Pending Appointments",
        "View Approved Appointments",
        "Set Working Hours",
        "Upload/View Medical Records",
        "Archived Appointments"
    ])
    # Columns definition for all appointments as reference
    columns = ["ID","Patient","Doctor","Date","StartTime","Duration","Status","Notes","Prescription","Feedback"]
    # Helper to pad appointments to 10 columns
    def pad_appts(appts, total_cols=10):
        padded = []
        for a in appts:
            padded.append(list(a) + [""]*(total_cols - len(a)))
        return padded
    # Fetch all doctor appointments
    all_appts = appt_db.get_doctor_appointments(username)
    #Pending Appointments 
    if menu == "View Pending Appointments":
        pending = [a for a in all_appts if a[6] == "pending"]
        df_pending = pd.DataFrame(pad_appts(pending), columns=columns) if pending else pd.DataFrame(columns=columns)
        show_dataframe_box(df_pending, "Pending Appointments")
        for appt in pending:
            st.markdown(f"**Patient:** {appt[1]} | **Date:** {appt[3]} {appt[4]} | **Duration:** {appt[5]} min")
            if st.button(f"Approve {appt[0]}", key=f"approve_{appt[0]}"):
                appt_db.update_status(appt[0], "approved")
                st.success("Approved!")
            if st.button(f"Deny {appt[0]}", key=f"deny_{appt[0]}"):
                appt_db.update_status(appt[0], "denied")
                st.warning("Denied")
    # Approved Appointments 
    elif menu == "View Approved Appointments":
        approved = [a for a in all_appts if a[6] == "approved"]
        df_approved = pd.DataFrame(pad_appts(approved), columns=columns) if approved else pd.DataFrame(columns=columns)
        show_dataframe_box(df_approved, "Approved Appointments")
        st.subheader(" Complete Appointment / Cancel")
        for appt in approved:
            st.markdown(f"**Patient:** {appt[1]} | **Date:** {appt[3]} {appt[4]} | **Duration:** {appt[5]} min")
            
            # Complete appointment form
            with st.form(f"complete_form_{appt[0]}"):
                prescription = st.text_area("Prescription", key=f"prescription_{appt[0]}")
                feedback = st.text_area("Feedback", key=f"feedback_{appt[0]}")
                complete_btn = st.form_submit_button("Complete Appointment")
                if complete_btn:
                    appt_db.complete_appointment(appt[0], prescription, feedback)
                    st.success("Appointment marked as completed and archived!")
            # Cancel button
            if st.button(f"Cancel Appointment {appt[0]}", key=f"cancel_{appt[0]}"):
                appt_db.update_status(appt[0], "cancelled")
                st.warning("Appointment cancelled.")
    #  Set Working Hours for doctor so that patient can schedule appointment within that time
    elif menu == "Set Working Hours":
        start_time = st.time_input("Start Time", value=format_time("09:00"))
        end_time = st.time_input("End Time", value=format_time("17:00"))
        if st.button("Save Hours"):
            doctor_db.set_hours(username, start_time.strftime("%H:%M"), end_time.strftime("%H:%M"))
            st.success("Working hours saved!")
    #  Archived Appointments 
    elif menu == "Archived Appointments":
        archived = appt_db.get_archived_appointments(username)
        df_archived = pd.DataFrame(pad_appts(archived), columns=columns) if archived else pd.DataFrame(columns=columns)
        show_dataframe_box(df_archived, "Archived Appointments")
   #  Upload and View Medical Records 
    elif menu == "Upload/View Medical Records":
        st.header("Upload Medical Records for Patients")
        patients = list({a[1] for a in all_appts})  # Unique patient usernames
        selected_patient = st.selectbox("Select Patient", patients, key="record_patient")
        uploaded_file = st.file_uploader("Upload Medical Record (PDF, Image, etc.)", type=['pdf','png','jpg','jpeg'], key="file_upload") # upload file
        if uploaded_file:
            save_dir = os.path.join("medical_records", selected_patient)
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File uploaded: {uploaded_file.name}")
        st.subheader("Existing Medical Records") # existing file
        patient_dir = os.path.join("medical_records", selected_patient)
        if os.path.exists(patient_dir):
            files = os.listdir(patient_dir)
            if files:
                for file in files:
                    file_path = os.path.join(patient_dir, file)
                    st.markdown(f"- {file}")
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="Download/View",
                            data=f,
                            file_name=file,
                            key=f"download_{file}"
                        )
            else:
                st.info("No records uploaded yet.")
        else:
            st.info("No records uploaded yet.")
