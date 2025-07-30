import pickle
# file_handler.py

patients = {}
bills = {}

def initialize_binary_files():
    """Initialize binary files for patients and bills."""
    try:
        with open('patients.dat', 'wb') as f:
            pickle.dump(patients, f)
        with open('bills.dat', 'wb') as f:
            pickle.dump(bills, f)
        return "Files initialized successfully."
    except Exception as e:
        return f"Error initializing files: {e}"

def save_bills():
    """Save bills to binary file."""
    try:
        with open('bills.dat', 'wb') as f:
            pickle.dump(bills, f)
        return "Bills saved successfully."
    except Exception as e:
        return f"Error saving bills: {e}"

def load_bills():
    """Load bills from binary file."""
    global bills
    try:
        with open('bills.dat', 'rb') as f:
            bills = pickle.load(f)
        return "Bills loaded successfully."
    except FileNotFoundError:
        return "No bill records found. Please create bills first."
    except Exception as e:
        return f"Error loading bills: {e}"

def load_patients():
    """Load patients from binary file."""
    global patients
    try:
        with open('patients.dat', 'rb') as f:
            patients = pickle.load(f)
        return "Patients loaded successfully."
    except FileNotFoundError:
        return "No patient records found. Please add patients first."
    except Exception as e:
        return f"Error loading patients: {e}"

# Load data at startup
load_patients()
load_bills()

# Function to add a patient
def add_patient(patient_id, name, age, gender, symptoms):
    if patient_id in patients:
        return "Patient already exists!"
    patients[patient_id] = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Symptoms": symptoms
    }
    return f"Patient {name} added successfully!"

def save_patients():
    """Save patients to binary file."""
    try:
        with open('patients.dat', 'wb') as f:
            pickle.dump(patients, f)
        return "Patients saved successfully."
    except Exception as e:
        return f"Error saving patients: {e}"

def create_bill(patient_id, consultation, lab, pharmacy):
    if patient_id not in patients:
        return "Patient not found."
    total = consultation + lab + pharmacy
    bills[patient_id] = {
        "Consultation": consultation,
        "Lab": lab,
        "Pharmacy": pharmacy,
        "Total": total
    }
    save_bills()
    bill_info = (
        f"Bill for {patients[patient_id]['Name']}:\n"
        f"Consultation: ${consultation}\n"
        f"Lab Charges: ${lab}\n"
        f"Pharmacy: ${pharmacy}\n"
        f"Total Bill: ${total}\n"
    )
    return bill_info

def view_bill(patient_id):
    if patient_id in bills:
        bill_details = f"--- Bill for {patients[patient_id]['Name']} ---\n"
        for key, value in bills[patient_id].items():
            bill_details += f"{key}: ${value}\n"
        return bill_details
    else:
        return "No bill found for this patient."

def search_patient(patient_id):
    if patient_id in patients:
        info = patients[patient_id]
        return (
            f"Patient Found: Name: {info['Name']}, Age: {info['Age']}, "
            f"Gender: {info['Gender']}, Symptoms: {info['Symptoms']}"
        )
    else:
        return "Patient not found."
