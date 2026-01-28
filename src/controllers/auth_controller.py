from src.models.user import User

class AuthController:
    def __init__(self, db):
        self.db = db

    def login(self, user_id, password):
        user_data = self.db.query_one("SELECT * FROM User WHERE UserID = ?", (user_id,))
        if user_data and user_data['Password'] == password:
            return User(user_data['UserID'], user_data['Email'], user_data['Password'], user_data['Role'])
        return None

    # --- HÀM 1: XÁC MINH DANH TÍNH (Bước 1) ---
    def verify_forgot_password(self, email, verify_id):
        """
        Kiểm tra xem Email và Mã xác thực có khớp không.
        Nếu đúng -> Trả về UserID (để cho phép đổi pass).
        Nếu sai -> Trả về None.
        """
        # 1. Tìm User theo Email
        user = self.db.query_one("SELECT * FROM User WHERE Email = ?", (email,))
        
        if not user:
            return None, " Error: Email not found in system."

        uid = user['UserID']
        role = user['Role']
        is_valid = False

        # 2. Logic kiểm tra (Giữ nguyên logic Admin = Username mà ông đã chốt)
        if role == 'student':
            check = self.db.query_one("SELECT * FROM Student WHERE UserID = ? AND StudentID = ?", (uid, verify_id))
            if check: is_valid = True
            
        elif role == 'lecturer':
            check = self.db.query_one("SELECT * FROM Lecturer WHERE UserID = ? AND LecturerID = ?", (uid, verify_id))
            if check: is_valid = True
            
        elif role == 'admin':
            # Admin dùng Username làm mã xác thực
            if verify_id == uid:
                is_valid = True

        if is_valid:
            return uid, " Identity Verified! Please enter new password."
        else:
            return None, " Error: ID does not match the Email provided."

    # --- HÀM 2: LƯU MẬT KHẨU MỚI (Bước 2) ---
    def reset_password(self, user_id, new_password):
        try:
            self.db.execute("UPDATE User SET Password = ? WHERE UserID = ?", (new_password, user_id))
            return True
        except:
            return False