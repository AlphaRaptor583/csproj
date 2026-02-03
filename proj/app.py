# Created by Himesh and Tanuj for CS Project Grade 12
# imports
import streamlit as st # main module for ui
from db.users import UserDB # database handling done using modules in db folder
from db.doctors import DoctorDB
from db.appointments import AppointmentDB
from ui.dashboard_patient import patient_dashboard # dashboards stored in ui folder
from ui.dashboard_doctor import doctor_dashboard
from ui.dashboard_admin import admin_dashboard

# list paths
db_path = "hospital_db.sqlite" # this is name of database
user_db = UserDB(db_path) # telling the database modules the path to database
doctor_db = DoctorDB(db_path)
appt_db = AppointmentDB(db_path)


ADMIN_USER = "a" # Hard code the admin credentials 
ADMIN_PASS = "a"

# Check if logged in or not
if "logged_in" not in st.session_state: 
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state: # role is admin, patient or doctor
    st.session_state.role = None
if "show_login_form" not in st.session_state:
    st.session_state.show_login_form = False
if "show_register_form" not in st.session_state:
    st.session_state.show_register_form = False

# First page/ Home page to allow login and registration of user
if not st.session_state.logged_in:
    st.title("GIIS Hospital Management System") # heading
    st.subheader("Please select an action:") # sub heading

    col1, col2 = st.columns(2) # create a table like structure but without a border so that buttons can be organised and placed in it
    with col1:
        if st.button("Login"):
            st.session_state.show_login_form = True # only show if parent button clicked
            st.session_state.show_register_form = False
    with col2:
        if st.button("Register"):
            st.session_state.show_register_form = True # only show if parent button is clicked
            st.session_state.show_login_form = False


    if st.session_state.show_login_form: # This is login form
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass") # since type is passpword, it hides the text being typed

        if st.button("Submit Login"): # Button to submit login pressed
            # Admin login
            if username == ADMIN_USER and password == ADMIN_PASS: # Check the hardcoded values for admin login
                st.session_state.logged_in = True
                st.session_state.username = username # save the details
                st.session_state.role = "admin"
                st.experimental_rerun() 
            
            user = user_db.authenticate(username, password) # if not logging in as admin, then check the database for the credentials
            if user: # authentication is actually done from db/database.py by first calling db/users.py and then that module in turn called db/database.py
                st.session_state.logged_in = True
                st.session_state.username = user[0]
                st.session_state.role = user[1] 
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")

  
    if st.session_state.show_register_form: # registration form is only for patient accounts
        st.subheader("Register New Patient Account") 
        new_user = st.text_input("Choose a new username in the format <firstnamelastname>", key="reg_user")
        new_pass = st.text_input("Choose a new Password", type="password", key="reg_pass")

        if st.button("Submit Registration"):
            ok, msg = user_db.register_user(new_user, new_pass) 
            if ok:
                st.success("Registered & automatically logged in!")
                st.session_state.logged_in = True
                st.session_state.username = new_user
                st.session_state.role = "patient"
                st.experimental_rerun()
            else:
                st.error(msg)

    st.stop()  # stop here if not logged in


st.sidebar.success(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
if st.sidebar.button("Logout"): # upon logig being successful, logout button is shown
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.experimental_rerun()

if st.session_state.role == "admin": # assign admin dashboard
    admin_dashboard(user_db, doctor_db, appt_db)
elif st.session_state.role == "doctor": # assign doctor dashboard
    doctor_dashboard(st.session_state.username, doctor_db, appt_db)
elif st.session_state.role == "patient": # assign patient dashboard
    patient_dashboard(st.session_state.username, doctor_db, appt_db)
