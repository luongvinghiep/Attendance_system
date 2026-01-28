import sqlite3

class Database:
    def __init__(self, db_file="attendance.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_data()

    def create_tables(self):
        # 1. USER (Base table - Khớp Class Diagram)
        self.execute('''CREATE TABLE IF NOT EXISTS User (
            UserID TEXT PRIMARY KEY,
            Email TEXT,
            Password TEXT,
            Role TEXT
        )''')
        
        # 2. STUDENT (Thêm FullName, BirthYear theo yêu cầu của bạn)
        self.execute('''CREATE TABLE IF NOT EXISTS Student (
            StudentID TEXT PRIMARY KEY,
            UserID TEXT,
            FullName TEXT,
            BirthYear INTEGER,
            Faculty TEXT,
            ClassName TEXT,
            FOREIGN KEY(UserID) REFERENCES User(UserID)
        )''')

        # 3. LECTURER (Thêm FullName, BirthYear)
        self.execute('''CREATE TABLE IF NOT EXISTS Lecturer (
            LecturerID TEXT PRIMARY KEY,
            UserID TEXT,
            FullName TEXT,
            BirthYear INTEGER,
            Faculty TEXT,
            FOREIGN KEY(UserID) REFERENCES User(UserID)
        )''')

        # 4. ADMIN
        self.execute('''CREATE TABLE IF NOT EXISTS Admin (
            AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID TEXT,
            AdminLevel INTEGER,
            FOREIGN KEY(UserID) REFERENCES User(UserID)
        )''')

        # 5. SUBJECT & CLASS (Học vụ)
        self.execute('''CREATE TABLE IF NOT EXISTS Subject (
            SubjectID TEXT PRIMARY KEY, SubjectName TEXT, Credits INTEGER
        )''')
        
        # Class mapping: LecturerID is assigned here (Sắp lớp dạy)
        self.execute('''CREATE TABLE IF NOT EXISTS Class (
            ClassID TEXT PRIMARY KEY,
            SubjectID TEXT,
            LecturerID TEXT, 
            FOREIGN KEY(SubjectID) REFERENCES Subject(SubjectID),
            FOREIGN KEY(LecturerID) REFERENCES Lecturer(LecturerID)
        )''')

        # 6. STUDENT_CLASS (Sắp lớp học cho sinh viên - Bảng trung gian)
        self.execute('''CREATE TABLE IF NOT EXISTS Student_Class (
            RegistrationID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID TEXT,
            ClassID TEXT,
            FOREIGN KEY(StudentID) REFERENCES Student(StudentID),
            FOREIGN KEY(ClassID) REFERENCES Class(ClassID)
        )''')
        
        # ... (Các bảng Schedule, AttendanceSession giữ nguyên như cũ) ...
        self.execute('''CREATE TABLE IF NOT EXISTS SystemConfig (ConfigKey TEXT PRIMARY KEY, ConfigValue TEXT)''')
        self.execute('''CREATE TABLE IF NOT EXISTS AttendanceRecord (RecordID INTEGER PRIMARY KEY, SessionID INTEGER, StudentID TEXT, Status TEXT, CheckInTime TEXT)''')
        self.execute('''CREATE TABLE IF NOT EXISTS AttendanceSession (SessionID INTEGER PRIMARY KEY, ClassID TEXT, AuthCode TEXT, StartTime TEXT, EndTime TEXT)''')


    def seed_data(self):
        # Tạo Admin mặc định
        check = self.query_one("SELECT * FROM User WHERE UserID = 'admin'")
        if not check:
            self.execute("INSERT INTO User VALUES ('admin', 'admin@uth.edu.vn', '123456', 'admin')")
            self.execute("INSERT INTO Admin (UserID, AdminLevel) VALUES ('admin', 1)")

    # Helper methods
    def query(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()
    def query_one(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()
    def execute(self, sql, params=()):
        self.cursor.execute(sql, params)
        self.conn.commit()