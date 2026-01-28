class ClassModel:
    def __init__(self, class_id, subject_id, lecturer_id):
        self.class_id = class_id
        self.subject_id = subject_id
        self.lecturer_id = lecturer_id
        self.student_list = [] # List chứa các sinh viên trong lớp

    def add_student(self, student):
        self.student_list.append(student)

    def __str__(self):
        return f"Class: {self.class_id} - Lecturer: {self.lecturer_id}"