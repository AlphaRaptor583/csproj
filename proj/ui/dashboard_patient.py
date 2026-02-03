import streamlit as st
from utils.display import show_dataframe_box
import datetime
import os
import pandas as pd
def patient_dashboard(username, doctor_db, appt_db):
    st.title("Patient Dashboard")
    st.header("Book Appointment")
    doctors = doctor_db.get_all_doctors()  # list of doctor usernames 
    selected_doctor = st.selectbox("Select Doctor", doctors, key="doctor_select") # select doctor
    # Get doctor working hours
    start_str, end_str = doctor_db.get_hours(selected_doctor) # get gours of selected doctor
    start_time = datetime.datetime.strptime(start_str or "09:00", "%H:%M").time()
    end_time = datetime.datetime.strptime(end_str or "17:00", "%H:%M").time()
    date = st.date_input("Appointment Date", min_value=datetime.date.today(), key="appt_date")
    time = st.time_input("Start Time", value=start_time, key="appt_time")
    duration = st.number_input("Duration (minutes)", min_value=10, max_value=180, step=5, key="appt_duration")
    if st.button("Book Appointment"): # book appointment
        if start_time <= time <= end_time:
            appt_db.add_appointment(username, selected_doctor, date.strftime("%Y-%m-%d"), time.strftime("%H:%M"), duration)
            st.success("Appointment requested! Waiting for doctor approval.")
        else:
            st.error(f"Time must be within doctor's working hours: {start_time}-{end_time}")
    st.header("Your Appointments") # Find my appointment
    all_appts = appt_db.get_patient_appointments(username)
    columns = ["ID","Patient","Doctor","Date","StartTime","Duration","Status","Notes","Prescription","Feedback"]
    def pad_appts(appts, total_cols=10):
        padded = []
        for a in appts:
            padded.append(list(a) + [""]*(total_cols - len(a)))
        return padded

    df_all = pd.DataFrame(pad_appts(all_appts), columns=columns) if all_appts else pd.DataFrame(columns=columns)
    show_dataframe_box(df_all, "All Appointments")
    # Show feedback and prescription for completed appointments
    st.header("Feedback & Prescription")
    completed_appts = [a for a in all_appts if a[6] == "completed"]
    if completed_appts:
        for appt in completed_appts:
            st.markdown(f"**Doctor:** {appt[2]} | **Date:** {appt[3]} {appt[4]}")
            st.markdown(f"- **Prescription:** {appt[8] or 'N/A'}")
            st.markdown(f"- **Feedback:** {appt[9] or 'N/A'}")
    else:
        st.info("No completed appointments yet.")
    # Last and next appointment displayed
    future_appts = [a for a in all_appts if a[3] >= datetime.date.today().strftime("%Y-%m-%d")]
    past_appts = [a for a in all_appts if a[3] < datetime.date.today().strftime("%Y-%m-%d")]

    if past_appts:
        last_date = max([a[3] for a in past_appts])
        st.info(f"Last Appointment Date: {last_date}")
    if future_appts:
        next_date = min([a[3] for a in future_appts])
        st.info(f"Next Appointment Date: {next_date}")

    #  Upload/View Medical Records 
    st.header("Medical Records")
    upload_file = st.file_uploader("Upload Medical Record (PDF/Image)", type=['pdf','png','jpg','jpeg'], key="patient_file")
    if upload_file:
        save_dir = os.path.join("medical_records", username)
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, upload_file.name)
        with open(file_path, "wb") as f:
            f.write(upload_file.getbuffer())
        st.success(f"File uploaded: {upload_file.name}")

    # Display existing records with download buttons
    patient_dir = os.path.join("medical_records", username)
    if os.path.exists(patient_dir):
        files = os.listdir(patient_dir)
        if files:
            st.subheader("Existing Records")
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
            st.info("No medical records uploaded yet.")
    else:
        st.info("No medical records uploaded yet.")
