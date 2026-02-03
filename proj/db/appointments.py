import sqlite3
class AppointmentDB: # appointment management queries
    def __init__(self, db_path="hospital_db.sqlite"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()
    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient TEXT NOT NULL,
                doctor TEXT NOT NULL,
                date DATE NOT NULL,
                start_time TEXT NOT NULL,
                duration INTEGER,
                status TEXT DEFAULT 'pending',
                doctor_notes TEXT,
                prescription TEXT,
                feedback TEXT
            )
        """)
        self.conn.commit()
    def add_appointment(self, patient, doctor, date, start_time, duration):
        self.cur.execute("""
            INSERT INTO appointments (patient, doctor, date, start_time, duration)
            VALUES (?, ?, ?, ?, ?)
        """, (patient, doctor, date, start_time, duration))
        self.conn.commit()
    def get_patient_appointments(self, patient):
        self.cur.execute("SELECT * FROM appointments WHERE patient=?", (patient,))
        return self.cur.fetchall()
    def get_doctor_appointments(self, doctor):
        self.cur.execute("SELECT * FROM appointments WHERE doctor=?", (doctor,))
        return self.cur.fetchall()
    def get_all_appointments(self):
        self.cur.execute("SELECT * FROM appointments")
        return self.cur.fetchall()
    def get_archived_appointments(self, doctor):
        self.cur.execute("SELECT * FROM appointments WHERE doctor=? AND status='completed'", (doctor,))
        return self.cur.fetchall()
    def get_archived_appointments_admin(self):
        self.cur.execute("SELECT * FROM appointments WHERE status='completed'")
        return self.cur.fetchall()
    def update_status(self, appt_id, status, notes=""):
        self.cur.execute("UPDATE appointments SET status=?, doctor_notes=? WHERE id=?", (status, notes, appt_id))
        self.conn.commit()
    def complete_appointment(self, appt_id, prescription="", feedback=""):
        self.cur.execute("""
            UPDATE appointments
            SET status='completed', prescription=?, feedback=?
            WHERE id=?
        """, (prescription, feedback, appt_id))
        self.conn.commit()
    def get_last_next_appointment(self, patient):
        self.cur.execute("SELECT * FROM appointments WHERE patient=? ORDER BY date ASC", (patient,))
        appts = self.cur.fetchall()
        completed = [a for a in appts if a[6] == "completed"]
        upcoming = [a for a in appts if a[6] in ["pending","approved","changed"]]
        last_appt = completed[-1] if completed else None
        next_appt = upcoming[0] if upcoming else None
        return last_appt, next_appt
