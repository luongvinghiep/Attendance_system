from src.utils import Utils

class AdminView:
    def __init__(self, controller, current_user):
        self.controller = controller
        self.current_user = current_user # Lưu user đang đăng nhập

    def show_menu(self):
        while True:
            Utils.clear_screen()
            # Hiện ID của Admin đang đăng nhập lên tiêu đề cho chuyên nghiệp
            Utils.print_header(f"ADMIN WORKSPACE ({self.current_user.user_id})")
            
            print("1. Manage Users")
            print("2. Manage Classes & Courses")
            print("3. System Configuration")
            print("4. View Attendance Report")
            print("5. Manage Profile (My Account)") # <--- MENU MỚI
            print("0. Logout")
            print("---------------------------")
            
            choice = input(">> Select function: ")
            
            if choice == '1': self.manage_users_menu()
            elif choice == '2': self.manage_classes_menu()
            elif choice == '3': self.config_ui()
            elif choice == '4': 
                print(self.controller.view_report())
                Utils.pause()
            elif choice == '5': self.manage_profile_menu() # <--- GỌI HÀM MỚI
            elif choice == '0': break
            else:
                Utils.print_error("Invalid selection!")
                Utils.pause()

    # --- MENU CON ---
    def manage_users_menu(self):
        while True:
            Utils.clear_screen()
            Utils.print_header("MANAGE USERS")
            print("1. Create New User (Student/Lecturer)")
            print("2. List All Users")
            print("0. Back")
            c = input(">> Select: ")
            if c == '1': self.create_user_ui()
            elif c == '2': 
                print(self.controller.list_users())
                Utils.pause()
            elif c == '0': break

    def manage_classes_menu(self):
        while True:
            Utils.clear_screen()
            Utils.print_header("MANAGE CLASSES")
            print("1. Add Subject")
            print("2. Create Class (Assign Lecturer)")
            print("3. Register Student to Class")
            print("0. Back")
            c = input(">> Select: ")
            if c == '1': self.add_subject_ui()
            elif c == '2': self.create_class_ui()
            elif c == '3': self.register_student_ui()
            elif c == '0': break

    def manage_profile_menu(self):
        while True:
            Utils.clear_screen()
            Utils.print_header("MY PROFILE")
            print(self.controller.get_admin_info(self.current_user.user_id))
            print("\n1. Change Password")
            print("0. Back")
            c = input(">> Select: ")
            if c == '1':
                p = input("Enter New Password: ")
                msg = self.controller.change_password(self.current_user.user_id, p)
                Utils.print_success(msg)
                Utils.pause()
            elif c == '0': break

    # --- INPUT UI ---
    def create_user_ui(self):
        print("\n--- SELECT ROLE ---")
        print("1. Student")
        print("2. Lecturer")
        role_opt = input(">> Choose (1/2): ").strip()
        if role_opt not in ['1', '2']: return

        print("\n--- ENTER DETAILS ---")
        uid = input("Username: ")
        email = input("Email: ")
        pwd = input("Password: ")
        full_name = input("Full Name: ")
        yob = input("Birth Year: ")
        
        extra_id, dept = "", ""
        if role_opt == '1':
            extra_id = input("Student ID: ")
            dept = input("Faculty: ")
        else:
            extra_id = input("Lecturer ID: ")
            dept = input("Faculty: ")

        msg = self.controller.create_user_flow(uid, email, pwd, role_opt, full_name, yob, extra_id, dept)
        Utils.print_success(msg)
        Utils.pause()

    def add_subject_ui(self):
        sid = input("Subject ID: ")
        name = input("Name: ")
        cre = input("Credits: ")
        print(self.controller.add_subject(sid, name, cre))
        Utils.pause()

    def create_class_ui(self):
        cid = input("Class ID: ")
        sid = input("Subject ID: ")
        lid = input("Lecturer ID: ")
        print(self.controller.create_class(cid, sid, lid))
        Utils.pause()

    def register_student_ui(self):
        sid = input("Student ID: ")
        cid = input("Class ID: ")
        print(self.controller.register_student(sid, cid))
        Utils.pause()

    def config_ui(self):
        key = input("Config Key: ")
        val = input("Config Value: ")
        print(self.controller.update_config(key, val))
        Utils.pause()