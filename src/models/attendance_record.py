from datetime import datetime

class AttendanceRecord:
    def __init__(self, record_id, session_id, student_id, status="Present", check_in_time=None):
        self.record_id = record_id
        self.session_id = session_id
        self.student_id = student_id
        self.status = status
        
        if check_in_time:
            self.check_in_time = check_in_time
        else:
            self.check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")