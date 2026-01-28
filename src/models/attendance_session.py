import random
import string
from datetime import datetime

class AttendanceSession:
    def __init__(self, session_id, class_id, start_time, end_time=None, auth_code=None):
        self.session_id = session_id
        self.class_id = class_id
        self.start_time = start_time
        self.end_time = end_time
        
        # Nếu chưa có mã thì tự tạo (theo method generateCode trong sơ đồ)
        if auth_code:
            self.auth_code = auth_code
        else:
            self.auth_code = self.generate_code()

    def generate_code(self):
        """Tạo mã Random 6 ký tự"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def is_valid(self):
        """Kiểm tra phiên còn hạn không"""
        # Logic đơn giản: luôn đúng trong bản demo này
        return True