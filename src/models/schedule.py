class Schedule:
    def __init__(self, schedule_id, class_id, room, start_time, end_time, day_of_week):
        self.schedule_id = schedule_id
        self.class_id = class_id
        self.room = room
        self.start_time = start_time
        self.end_time = end_time
        self.day_of_week = day_of_week 

    def get_day_name(self):
        days = {2: "Monday", 3: "Tuesday", 4: "Wednesday", 5: "Thursday", 6: "Friday", 7: "Saturday", 8: "Sunday"}
        return days.get(int(self.day_of_week), "Unknown")