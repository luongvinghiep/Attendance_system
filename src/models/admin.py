from src.models.user import User

class Admin(User):
    def __init__(self, user_id, email, password, admin_level=1):
        super().__init__(user_id, email, password, "admin")
        self.admin_level = admin_level

    def view_system_logs(self):
        # Mô phỏng phương thức trong sơ đồ lớp
        return "Displaying system logs..."