import pandas as pd

from config import pg_db_conn as pg_db_conn
from utils import utils, date_utility


def get_all_schedule_assignments_by_student(student_user_id):
    """Get all course data from the database"""
    sql = """
        select usaur.*, 
            us.id us_id, us.user_id, us.task_id, us.start_date, us.end_date, us.completion_percentage, us.status, us.update,
            task.task_type, task.task_name, task.task_score, task.task_due_date,
            cyn.academic_year, course.subject, course.course_name, cyn.room_number, 
            student.id as student_id, student.first_name || ' ' || student.last_name as student_name,
            assigned_user.id as assigned_user_id, assigned_user.first_name || ' ' || assigned_user.last_name as assigned_user_name,
            user_reln.reln_type,
            teacher.id as teacher_id, teacher.first_name || ' ' || teacher.last_name as teacher_name
        from student_incentive_plan.user_schedule_assigned_user_reln usaur
            inner join student_incentive_plan.user_schedule us on usaur.user_schedule_id = us.id
            inner join student_incentive_plan.user student on student."id" = us.user_id
            inner join student_incentive_plan.user assigned_user on assigned_user."id" = usaur.assigned_user_id
            inner join student_incentive_plan.task task on task.id = us.task_id
            inner join student_incentive_plan.course_year_reln cyn on task.year_course_reln_id = cyn.id
            inner join student_incentive_plan.course course on course."id" = cyn.course_id
            inner join student_incentive_plan.user teacher on teacher."id" = cyn.teacher_id
            inner join student_incentive_plan.user_reln user_reln on user_reln.primary_user_id = student.id and user_reln.related_user_id = assigned_user.id
        where task.year_course_reln_id in (select year_course_reln_id from student_incentive_plan.user_course_reln where user_id = {})
            and us.status NOT IN ('X')
        order by academic_year, course.subject, course.course_name
    """.format(student_user_id)
    results = pg_db_conn.execute_query(sql)
    return results


def get_all_schedule_assignments_to_user(assigned_to_user_id):
    """Get all course data from the database"""
    sql = """
        select usaur.*, 
            us.id us_id, us.user_id, us.task_id, us.start_date, us.end_date, us.completion_percentage, us.status, us.update,
            task.task_type, task.task_name, task.task_score, task.task_due_date,
            cyn.academic_year, course.subject, course.course_name, cyn.room_number, 
            student.id as student_id, student.first_name || ' ' || student.last_name as student_name,
            assigned_user.id as assigned_user_id, assigned_user.first_name || ' ' || assigned_user.last_name as assigned_user_name,
            user_reln.reln_type,
            teacher.id as teacher_id, teacher.first_name || ' ' || teacher.last_name as teacher_name
        from student_incentive_plan.user_schedule_assigned_user_reln usaur
            inner join student_incentive_plan.user_schedule us on usaur.user_schedule_id = us.id
            inner join student_incentive_plan.user student on student."id" = us.user_id
            inner join student_incentive_plan.user assigned_user on assigned_user."id" = usaur.assigned_user_id
            inner join student_incentive_plan.task task on task.id = us.task_id
            inner join student_incentive_plan.course_year_reln cyn on task.year_course_reln_id = cyn.id
            inner join student_incentive_plan.course course on course."id" = cyn.course_id
            inner join student_incentive_plan.user teacher on teacher."id" = cyn.teacher_id
            inner join student_incentive_plan.user_reln user_reln on user_reln.primary_user_id = student.id and user_reln.related_user_id = assigned_user.id
        where usaur.assigned_user_id = {}
            and us.status NOT IN ('X')
        order by academic_year, course.subject, course.course_name
    """.format(assigned_to_user_id)
    results = pg_db_conn.execute_query(sql)
    return results


def add_assigned_user_for_schedule(user_schedule_id, assigned_user_id, assigned_user_comments):
    """Assign a user to a user schedule"""
    sql = """
        insert into student_incentive_plan.user_schedule_assigned_user_reln (id, user_schedule_id, assigned_user_id, assigned_user_comments, status)
        values ({}, {}, {}, '{}', '{}')
    """.format(utils.get_unique_id(), user_schedule_id, assigned_user_id, assigned_user_comments, 'A')
    ret_sts = pg_db_conn.save_query(sql)
    return ret_sts


def update_user_schedule_assign_feedback(id, assigned_user_comments):
    """Update the feedback for a user schedule assignment"""
    sql = """
        update student_incentive_plan.user_schedule_assigned_user_reln
        set assigned_user_comments = '{}'
        where id = {}
    """.format(assigned_user_comments, id)
    ret_sts = pg_db_conn.save_query(sql)
    return ret_sts


def get_assigned_schedule_by_id(id):
    """Get all course data from the database"""
    sql = """
        select usaur.*, 
            us.id us_id, us.user_id, us.task_id, us.start_date, us.end_date, us.completion_percentage, us.status, us.update,
            task.task_type, task.task_name, task.task_score, task.task_due_date,
            cyn.academic_year, course.subject, course.course_name, cyn.room_number, 
            student.id as student_id, student.first_name || ' ' || student.last_name as student_name,
            assigned_user.id as assigned_user_id, assigned_user.first_name || ' ' || assigned_user.last_name as assigned_user_name,
            user_reln.reln_type,
            teacher.id as teacher_id, teacher.first_name || ' ' || teacher.last_name as teacher_name
        from student_incentive_plan.user_schedule_assigned_user_reln usaur
            inner join student_incentive_plan.user_schedule us on usaur.user_schedule_id = us.id
            inner join student_incentive_plan.user student on student."id" = us.user_id
            inner join student_incentive_plan.user assigned_user on assigned_user."id" = usaur.assigned_user_id
            inner join student_incentive_plan.task task on task.id = us.task_id
            inner join student_incentive_plan.course_year_reln cyn on task.year_course_reln_id = cyn.id
            inner join student_incentive_plan.course course on course."id" = cyn.course_id
            inner join student_incentive_plan.user teacher on teacher."id" = cyn.teacher_id
            inner join student_incentive_plan.user_reln user_reln on user_reln.primary_user_id = student.id and user_reln.related_user_id = assigned_user.id
        where usaur.id = {}
    """.format(id)
    results = pg_db_conn.execute_query(sql)
    return results