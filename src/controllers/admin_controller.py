from tabulate import tabulate
# --- IMPORT MODELS ---
from src.models.user import User
from src.models.student import Student
from src.models.lecturer import Lecturer
from src.models.subject import Subject          # <--- Mới thêm
from src.models.class_model import ClassModel   # <--- Mới thêm (Lưu ý tên file là class_model)

class AdminController:
    def __init__(self, db):
        self.db = db

    # --- USE CASE 1: MANAGE USERS ---
    def create_user_flow(self, user_id, email, password, role_opt, full_name, birth_year, extra_id, dept):
        try:
            # [OOP STEP 1]: Khởi tạo Object trước
            if role_opt == '1': # STUDENT
                new_student = Student(user_id, email, password, extra_id, full_name, birth_year, dept, class_name="")
                
                # [OOP STEP 2]: Lưu dữ liệu TỪ OBJECT xuống DB (Không dùng biến thô)
                self.db.execute("INSERT INTO User VALUES (?, ?, ?, ?)", 
                               (new_student.user_id, new_student.email, new_student.password, new_student.role))
                self.db.execute("INSERT INTO Student (StudentID, UserID, FullName, BirthYear, Faculty, ClassName) VALUES (?, ?, ?, ?, ?, ?)",
                               (new_student.student_id, new_student.user_id, new_student.full_name, new_student.birth_year, new_student.faculty, new_student.class_name))
                
            elif role_opt == '2': # LECTURER
                new_lecturer = Lecturer(user_id, email, password, extra_id, full_name, birth_year, dept)
                
                # [OOP STEP 2]: Lưu dữ liệu TỪ OBJECT xuống DB
                self.db.execute("INSERT INTO User VALUES (?, ?, ?, ?)", 
                               (new_lecturer.user_id, new_lecturer.email, new_lecturer.password, new_lecturer.role))
                self.db.execute("INSERT INTO Lecturer (LecturerID, UserID, FullName, BirthYear, Faculty) VALUES (?, ?, ?, ?, ?)",
                               (new_lecturer.lecturer_id, new_lecturer.user_id, new_lecturer.full_name, new_lecturer.birth_year, new_lecturer.faculty))
            
            return " Success: User created successfully (OOP Standard)!"
        except Exception as e:
            return f" Error: {str(e)}"

    def list_users(self):
        sql = """
            SELECT User.UserID, User.Role, Student.FullName FROM User JOIN Student ON User.UserID = Student.UserID
            UNION
            SELECT User.UserID, User.Role, Lecturer.FullName FROM User JOIN Lecturer ON User.UserID = Lecturer.UserID
        """
        data = self.db.query(sql)
        return tabulate(data, headers=["UserID", "Role", "Full Name"], tablefmt="grid")

    # --- USE CASE 2: MANAGE CLASSES & COURSES ---
    def add_subject(self, sub_id, name, credits):
        try:
            # [OOP STEP 1]: Tạo Object Subject từ Model
            new_subject = Subject(sub_id, name, credits)
            
            # [OOP STEP 2]: Lưu dữ liệu từ Object new_subject xuống DB
            self.db.execute("INSERT INTO Subject VALUES (?, ?, ?)", 
                           (new_subject.subject_id, new_subject.subject_name, new_subject.credits))
            
            return " Success: Subject added (Verified by Model)."
        except: return " Error: Subject ID already exists."

    def create_class(self, class_id, sub_id, lecturer_id):
        # Validate Lecturer existence
        lec = self.db.query_one("SELECT * FROM Lecturer WHERE LecturerID = ?", (lecturer_id,))
        if not lec: return " Error: Lecturer ID not found."
        
        try:
            # [OOP STEP 1]: Tạo Object ClassModel
            new_class = ClassModel(class_id, sub_id, lecturer_id)
            
            # [OOP STEP 2]: Lưu dữ liệu từ Object new_class xuống DB
            self.db.execute("INSERT INTO Class (ClassID, SubjectID, LecturerID) VALUES (?, ?, ?)", 
                           (new_class.class_id, new_class.subject_id, new_class.lecturer_id))
            
            return f" Success: Class {new_class.class_id} initialized."
        except Exception as e: return f" Error: Failed to create class. {str(e)}"

    def register_student(self, student_id, class_id):
        # Validate existence
        stu = self.db.query_one("SELECT * FROM Student WHERE StudentID = ?", (student_id,))
        cls = self.db.query_one("SELECT * FROM Class WHERE ClassID = ?", (class_id,))
        
        if not stu: return " Error: Student ID not found."
        if not cls: return " Error: Class ID not found."

        try:
            # Note: Student_Class là bảng trung gian (Association Table), 
            # thường không cần Model riêng trừ khi có logic phức tạp.
            # Ở đây ta lưu trực tiếp ID là chấp nhận được trong mô hình này.
            self.db.execute("INSERT INTO Student_Class (StudentID, ClassID) VALUES (?, ?)", (student_id, class_id))
            return f" Success: Student {student_id} added to Class {class_id}."
        except: return " Error: Student already in this class."

    # --- USE CASE 3 & 4: CONFIG & REPORT ---
    def update_config(self, key, value):
        self.db.execute("INSERT OR REPLACE INTO SystemConfig VALUES (?, ?)", (key, value))
        return " Success: Configuration saved."

    def view_report(self):
        u_count = self.db.query_one("SELECT COUNT(*) as c FROM User")['c']
        c_count = self.db.query_one("SELECT COUNT(*) as c FROM Class")['c']
        s_count = self.db.query_one("SELECT COUNT(*) as c FROM Student_Class")['c']
        return f"\n=== REPORT ===\nTotal Users: {u_count}\nTotal Classes: {c_count}\nRegistrations: {s_count}"

    # --- USE CASE 5: MANAGE PROFILE ---
    def get_admin_info(self, user_id):
        # [OOP Handling]: Dùng Model Admin để xử lý logic hiển thị nếu cần thiết
        sql = "SELECT User.UserID, User.Email, User.Role, Admin.AdminLevel FROM User JOIN Admin ON User.UserID = Admin.UserID WHERE User.UserID = ?"
        data = self.db.query_one(sql, (user_id,))
        if data:
            return f"\n=== MY PROFILE ===\nID: {data['UserID']}\nEmail: {data['Email']}\nRole: {data['Role']}\nLevel: {data['AdminLevel']}"
        return "Error: Profile not found."

    def change_password(self, user_id, new_pass):
        try:
            self.db.execute("UPDATE User SET Password = ? WHERE UserID = ?", (new_pass, user_id))
            return " Success: Password changed!"
        except Exception as e: return f" Error: {str(e)}"