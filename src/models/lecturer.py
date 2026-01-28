from src.models.user import User

class Lecturer(User):
    def __init__(self, user_id, email, password, lecturer_id, full_name, birth_year, faculty):
        super().__init__(user_id, email, password, "lecturer")
        self.lecturer_id = lecturer_id
        self.full_name = full_name
        self.birth_year = birth_year
        self.faculty = faculty