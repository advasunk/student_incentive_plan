import pandas as pd

from config import pg_db_conn as pg_db_conn
from utils import utils, date_utility


def get_all_schedules_by_user(user_id):
    """Get all course data from the database"""
    sql = """
        select us.*,
            task.task_type, task.task_name, task.task_score, task.task_due_date,
            cyn.academic_year, c.subject, c.course_name, cyn.room_number, u.first_name || ' ' || u.last_name as teacher_name
        from student_incentive_plan.user_schedule us
            inner join student_incentive_plan.task task on task.id = us.task_id
            inner join student_incentive_plan.course_year_reln cyn on task.year_course_reln_id = cyn.id
            inner join student_incentive_plan.course c on c."id" = cyn.course_id
            inner join student_incentive_plan.user u on u."id" = cyn.teacher_id
        where task.year_course_reln_id in (select year_course_reln_id from student_incentive_plan.user_course_reln where user_id = {})
        and us.status is null or us.status = '' or  us.status NOT IN ('X')
        and us.user_id = {}
        order by academic_year, c.subject, c.course_name
    """.format(user_id, user_id)
    results = pg_db_conn.execute_query(sql)
    return results


def update_user_schedule(user_schedule_id, start_date, end_date, completion_percentage):
    """Update user_schedule with new data"""
    sql = """
        update student_incentive_plan.user_schedule set
            start_date = '{}',
            end_date = '{}',
            completion_percentage = {}
        where id = {}
    """.format(start_date, end_date, completion_percentage, user_schedule_id)
    ret_sts = pg_db_conn.save_query(sql)
    return ret_sts


def delete_user_schedule(user_schedule_id):
    """Update user_schedule with new data"""
    sql = """
        update student_incentive_plan.user_schedule set
        status = 'X'
        where id = {}
    """.format(user_schedule_id)
    ret_sts = pg_db_conn.save_query(sql)
    return ret_sts


def add_schedule_for_task(user_id, task_data):
    # set start_date to today's date in yyyy-mm-dd format
    start_date = date_utility.get_current_date()
    """Add schedule for task"""
    sql = """
        insert into student_incentive_plan.user_schedule (id, user_id, task_id, start_date, end_date, completion_percentage, status)
        values ({}, {}, {}, '{}', '{}', {}, '{}')
    """.format(utils.get_unique_id(), user_id, task_data['id'], start_date, task_data['task_due_date'], 0, 'A')
    ret_sts = pg_db_conn.save_query(sql)
    return ret_sts


def get_schedule_by_id(user_schedule_id):
    """Get all course data from the database"""
    sql = """
        select us.*,
            task.task_type, task.task_name, task.task_score, task.task_due_date,
            cyn.academic_year, c.subject, c.course_name, cyn.room_number, u.first_name || ' ' || u.last_name as teacher_name
        from student_incentive_plan.user_schedule us
            inner join student_incentive_plan.task task on task.id = us.task_id
            inner join student_incentive_plan.course_year_reln cyn on task.year_course_reln_id = cyn.id
            inner join student_incentive_plan.course c on c."id" = cyn.course_id
            inner join student_incentive_plan.user u on u."id" = cyn.teacher_id
        where us.id = {}
    """.format(user_schedule_id)
    results = pg_db_conn.execute_query(sql)
    return results
