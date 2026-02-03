import sqlite3
class DoctorDB: # contains queries for doctors
    def __init__(self, db_path="hospital_db.sqlite"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_tables()
    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS doctor_hours (
                doctor TEXT PRIMARY KEY,
                start_time TEXT,
                end_time TEXT
            )
        """)
        self.conn.commit()
    def get_all_doctors(self):
        self.cur.execute("SELECT username FROM users WHERE role='doctor'")
        rows = self.cur.fetchall()
        return [r[0] for r in rows]
    def set_hours(self, doctor, start_time, end_time):
        self.cur.execute("""
            INSERT INTO doctor_hours (doctor, start_time, end_time)
            VALUES (?, ?, ?)
            ON CONFLICT(doctor) DO UPDATE SET start_time=excluded.start_time, end_time=excluded.end_time
        """, (doctor, start_time, end_time))
        self.conn.commit()
    def get_hours(self, doctor):
        self.cur.execute("SELECT start_time, end_time FROM doctor_hours WHERE doctor=?", (doctor,))
        row = self.cur.fetchone()
        if row:
            return row[0], row[1]
        return "09:00", "17:00"
