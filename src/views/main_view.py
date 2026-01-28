from src.utils import Utils
from src.views.admin_view import AdminView
from src.controllers.admin_controller import AdminController

# Placeholder imports
# from src.views.student_view import StudentView
# from src.views.lecturer_view import LecturerView

class MainView:
    def __init__(self, auth_controller, db):
        self.auth = auth_controller
        self.db = db

    def show_login_screen(self):
        while True:
            Utils.clear_screen()
            print(" STUDENT ATTENDANCE SYSTEM (UTH)")
            print("-------------------------------------")
            print("1. Login")
            print("2. Forgot Password") # Đã đổi thành Tiếng Anh
            print("0. Exit")
            print("-------------------------------------")
            
            choice = input(">> Select option: ")
            
            if choice == '1':
                self.handle_login()
            elif choice == '2':
                self.handle_forgot_password()
            elif choice == '0':
                Utils.print_success("Goodbye!")
                break
            else:
                Utils.print_error("Invalid option!")
                Utils.pause()

    def handle_login(self):
        Utils.print_header("LOGIN SYSTEM")
        user_id = input("Username (UserID): ").strip()
        password = Utils.input_password("Password: ")
        
        user = self.auth.login(user_id, password)
        
        if user:
            Utils.print_success(f"Welcome back, {user.role.upper()}!")
            Utils.pause()
            self.navigate_to_role_view(user)
        else:
            Utils.print_error("Invalid Username or Password!")
            Utils.pause()

    def handle_forgot_password(self):
        Utils.print_header("FORGOT PASSWORD")
        print("(Reset Password via Email & Verification)")
        
        email = input("Enter Email: ").strip()
        
        print("\n--- VERIFICATION REQUIRED ---")
        print("• Student  -> Enter Student ID")
        print("• Lecturer -> Enter Lecturer ID")
        print("• Admin    -> Enter Username")
        
        verify_input = input(">> Enter ID / Key: ").strip()
        
        # BƯỚC 1: Gọi controller xác minh
        user_id, msg = self.auth.verify_forgot_password(email, verify_input)
        
        if user_id:
            # Nếu xác minh thành công (có user_id trả về)
            Utils.print_success(msg)
            
            # BƯỚC 2: Nhập mật khẩu mới
            print("\n--- RESET PASSWORD ---")
            new_pass = input("Enter New Password: ").strip()
            confirm_pass = input("Confirm New Password: ").strip()
            
            if new_pass == confirm_pass and new_pass != "":
                # BƯỚC 3: Lưu vào DB
                if self.auth.reset_password(user_id, new_pass):
                    Utils.print_success(" Password has been changed successfully!")
                    print(">> Please login with your new password.")
                else:
                    Utils.print_error(" Database Error: Could not update password.")
            else:
                Utils.print_error(" Error: Passwords do not match or empty.")
        else:
            # Nếu xác minh thất bại
            Utils.print_error(msg)
        
        Utils.pause()

    def navigate_to_role_view(self, user):
        if user.role == 'admin':
            ctrl = AdminController(self.db)
            view = AdminView(ctrl)
            view.show_menu()
        elif user.role == 'student':
            Utils.print_warning("Student View is under construction...")
            Utils.pause()
        elif user.role == 'lecturer':
            Utils.print_warning("Lecturer View is under construction...")
            Utils.pause()
    def navigate_to_role_view(self, user):
        if user.role == 'admin':
            ctrl = AdminController(self.db)
            # QUAN TRỌNG: Thêm biến 'user' vào đây
            view = AdminView(ctrl, user) 
            view.show_menu()
            
        elif user.role == 'student':
            Utils.print_warning("Student View is under construction...")
            Utils.pause()
            
        elif user.role == 'lecturer':
            Utils.print_warning("Lecturer View is under construction...")
            Utils.pause()