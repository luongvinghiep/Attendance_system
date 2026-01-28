class User:
    def __init__(self, user_id, email, password, role):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.role = role
    def __str__(self):
        return f"User: {self.user_id} | Role: {self.role}"