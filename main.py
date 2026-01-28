from src.database import Database
from src.controllers.auth_controller import AuthController
from src.views.main_view import MainView

def main():
    # 1. Khởi động Database (Tự tạo bảng & Admin mặc định)
    db = Database()
    
    # 2. Khởi động Auth
    auth = AuthController(db)
    
    # 3. Chạy màn hình chính
    app = MainView(auth, db)
    app.show_login_screen()

if __name__ == "__main__":
    main()