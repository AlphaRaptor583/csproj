import streamlit as st
from utils.display import show_dataframe_box
import pandas as pd

def admin_dashboard(user_db, doctor_db, appt_db):
    st.title("Admin Dashboard")
    menu = st.selectbox("Select Action", [
        "View Users",
        "Change Roles",
        "View All Appointments",
        "Archived Appointments"
    ])
    if menu == "View Users": # view user menu
        df = user_db.get_all_accounts()
        show_dataframe_box(df, "All User Accounts")
    elif menu == "Change Roles": # change role menu
        df = user_db.get_all_accounts()
        users = df["Username"].tolist()
        selected_user = st.selectbox("Select User", users)
        new_role = st.selectbox("New Role", ["patient", "doctor", "admin"])
        if st.button("Update Role"):
            user_db.update_role(selected_user, new_role)
            st.success(f"{selected_user} → {new_role}")
    elif menu == "View All Appointments": # view all appointment menu
        appts = appt_db.get_all_appointments()
        columns = ["ID","Patient","Doctor","Date","StartTime","Duration","Status","Notes","Prescription","Feedback"]
        def pad_appts(appts, total_cols=10):
            padded = []
            for a in appts:
                padded.append(list(a) + [""]*(total_cols - len(a)))
            return padded
        df_all = pd.DataFrame(pad_appts(appts), columns=columns) if appts else pd.DataFrame(columns=columns)
        show_dataframe_box(df_all, "All Appointments")
        approved_appts = [a for a in appts if a[6] == "approved"] # cancel appointment
        for appt in approved_appts:
            st.markdown(f"**Patient:** {appt[1]} | **Doctor:** {appt[2]} | **Date:** {appt[3]} {appt[4]} | **Duration:** {appt[5]} min")
            if st.button(f"Cancel {appt[0]}", key=f"admin_cancel_{appt[0]}"):
                appt_db.update_status(appt[0], "cancelled")
                st.warning("Appointment cancelled!")
    elif menu == "Archived Appointments": # archived or completed appointment
        archived = appt_db.get_archived_appointments_admin()
        columns = ["ID","Patient","Doctor","Date","StartTime","Duration","Status","Notes","Prescription","Feedback"]
        def pad_appts(appts, total_cols=10):
            padded = []
            for a in appts:
                padded.append(list(a) + [""]*(total_cols - len(a)))
            return padded
        df_archived = pd.DataFrame(pad_appts(archived), columns=columns) if archived else pd.DataFrame(columns=columns)
        show_dataframe_box(df_archived, "Archived Appointments")
