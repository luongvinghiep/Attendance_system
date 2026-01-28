from src.models.user import User

class Student(User):
    # Khớp sơ đồ Class + Yêu cầu thêm Tên/Năm sinh
    def __init__(self, user_id, email, password, student_id, full_name, birth_year, faculty, class_name):
        super().__init__(user_id, email, password, "student")
        self.student_id = student_id
        self.full_name = full_name
        self.birth_year = birth_year
        self.faculty = faculty
        self.class_name = class_name