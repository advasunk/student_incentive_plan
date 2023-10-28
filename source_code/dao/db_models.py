class user:
    def __init__(self,
                 id, first_name, last_name, email, password, date_of_birth, user_type, user_group, is_active):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.user_type = user_type
        self.user_group = user_group
        self.is_active = is_active


class user_course_reln:
    def __init__(self,
                 id, user_id, year_course_reln_id):
        self.id = id
        self.user_id = user_id
        self.year_course_reln_id = year_course_reln_id


class user_schedule:
    def __init__(self,
                 id, user_id, task_id, start_date, end_date, completion_percentage, status, update):
        self.id = id
        self.user_id = user_id
        self.task_id = task_id
        self.start_date = start_date
        self.end_date = end_date
        self.completion_percentage = completion_percentage
        self.status = status
        self.update = update


class user_schedule_assigned_user_reln:
    def __init__(self,
                 id, user_schedule_id, assigned_user_id, assigned_user_comments):
        self.id = id
        self.user_schedule_id = user_schedule_id
        self.assigned_user_id = assigned_user_id
        self.assigned_user_comments = assigned_user_comments


class course:
    def __init__(self,
                 id, course_name, subject, course_description):
        self.id = id
        self.course_name = course_name
        self.subject = subject
        self.course_description = course_description


class course_year_reln:
    def __init__(self,
                 id, academic_year, course_id, teacher_id, room_number):
        self.id = id
        self.academic_year = academic_year
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.room_number = room_number


class task:
    def __init__(self,
                 id, year_course_reln_id, task_name, task_type, task_description, task_due_date, task_score):
        self.id = id
        self.year_course_reln_id = year_course_reln_id
        self.task_name = task_name
        self.task_type = task_type
        self.task_description = task_description
        self.task_due_date = task_due_date
        self.task_score = task_score
