class Subject:
    def __init__(self, subject_id, subject_name, credits):
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.credits = int(credits)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_id})"