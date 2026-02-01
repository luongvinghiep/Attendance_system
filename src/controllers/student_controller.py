from datetime import datetime
from src.models.attendance_record import AttendanceRecord

class StudentController:
    def __init__(self, db):
        self.db = db

    # ==========================
    # UC-03: MARK ATTENDANCE
    # ==========================
    def mark_attendance(self, student_id, auth_code):
        """
        Sinh viên nhập mã điểm danh (auth_code)
        """

        # --- CHECK 1: Mã điểm danh có tồn tại không ---
        session = self.db.query_one(
            "SELECT * FROM AttendanceSession WHERE AuthCode = ?",
            (auth_code,)
        )
        if not session:
            return " Error: Attendance code does not exist."

        session_id = session["SessionID"]
        class_id = session["ClassID"]

        # --- CHECK 2: Session còn hiệu lực không ---
        if session.get("EndTime") is not None:
            return " Error: Attendance session has ended."

        # --- CHECK 3: Sinh viên có thuộc lớp này không ---
        enrolled = self.db.query_one(
            "SELECT * FROM Student_Class WHERE StudentID = ? AND ClassID = ?",
            (student_id, class_id)
        )
        if not enrolled:
            return " Error: You are not registered in this class."

        # --- CHECK 4: Sinh viên đã điểm danh chưa ---
        existed = self.db.query_one(
            "SELECT * FROM AttendanceRecord WHERE SessionID = ? AND StudentID = ?",
            (session_id, student_id)
        )
        if existed:
            return " Error: Attendance already recorded."

        # --- GHI NHẬN ĐIỂM DANH ---
        record = AttendanceRecord(
            record_id=None,
            session_id=session_id,
            student_id=student_id,
            status="Present",
            check_in_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self.db.execute(
            """
            INSERT INTO AttendanceRecord (SessionID, StudentID, Status, CheckInTime)
            VALUES (?, ?, ?, ?)
            """,
            (
                record.session_id,
                record.student_id,
                record.status,
                record.check_in_time
            )
        )

        return " Success: Attendance recorded successfully!"
