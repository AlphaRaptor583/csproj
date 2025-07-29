import pickle
# file_handler.py

patients = {}
bills = {}
# e
# Function to add a patient
def add_patient():
    patient_id = input("Enter Patient ID: ")
    if patient_id in patients:
        print("Patient already exists!")
        return
    name = input("Enter Patient Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender (Male/Female/Other): ")
    symptoms = input("Enter Symptoms: ")

    patients[patient_id] = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Symptoms": symptoms
    }
    print(f"\n✅ Patient {name} added successfully!\n")

# Function to display all patients
def display_patients():
    if not patients:
        print("❗ No patient records found.")
        return
    print("\n--- All Patient Records ---")
    for pid, info in patients.items():
        print(f"ID: {pid} | Name: {info['Name']} | Age: {info['Age']} | Gender: {info['Gender']} | Symptoms: {info['Symptoms']}")

# Function to create a bill for a patient
def create_bill():
    patient_id = input("Enter Patient ID: ")
    if patient_id not in patients:
        print("❗ Patient not found.")
        return
    
    consultation = float(input("Enter Consultation Fee: $"))
    lab = float(input("Enter Lab Charges: $"))
    pharmacy = float(input("Enter Pharmacy Charges: $"))

    total = consultation + lab + pharmacy

    bills[patient_id] = {
        "Consultation": consultation,
        "Lab": lab,
        "Pharmacy": pharmacy,
        "Total": total
    }

    print(f"\n💰 Bill for {patients[patient_id]['Name']}:")
    print(f"Consultation: ${consultation}")
    print(f"Lab Charges: ${lab}")
    print(f"Pharmacy: ${pharmacy}")
    print(f"🧾 Total Bill: ${total}\n")

# Function to view a patient's bill
def view_bill():
    patient_id = input("Enter Patient ID: ")
    if patient_id in bills:
        print(f"\n--- Bill for {patients[patient_id]['Name']} ---")
        for key, value in bills[patient_id].items():
            print(f"{key}: ${value}")
    else:
        print("❗ No bill found for this patient.")

# Function to search patient
def search_patient():
    patient_id = input("Enter Patient ID: ")
    if patient_id in patients:
        info = patients[patient_id]
        print(f"\n👤 Patient Found: Name: {info['Name']}, Age: {info['Age']}, Gender: {info['Gender']}, Symptoms: {info['Symptoms']}")
    else:
        print("❗ Patient not found.")

# Menu-driven program
def main():
    while True:
        print("\n--- Hospital Management System ---")
        print("1. Add Patient")
        print("2. Display All Patients")
        print("3. Create Bill")
        print("4. View Bill")
        print("5. Search Patient")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            display_patients()
        elif choice == "3":
            create_bill()
        elif choice == "4":
            view_bill()
        elif choice == "5":
            search_patient()
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 6.")
pickle.dump 
# Run the program
if __name__ == "__main__":
    main()