import pandas as pd

from config import pg_db_conn as pg_db_conn
from utils import utils


def get_all_tasks_by_course():
    """Get all course data from the database"""
    sql = """
        select
        t."id", t.task_description,
        t.task_name, t.task_score, t.task_type,
        t.task_due_date, t.year_course_reln_id,
        cyn.academic_year, c.subject, c.course_name, cyn.room_number, u.first_name || ' ' || u.last_name as teacher_name
        from student_incentive_plan.task t 
        inner join student_incentive_plan.course_year_reln cyn on t.year_course_reln_id = cyn.id
        inner join student_incentive_plan.course c on c."id" = cyn.course_id
        inner join student_incentive_plan.user u on u."id" = cyn.teacher_id
        order by academic_year, c.subject, c.course_name
    """
    results = pg_db_conn.execute_query(sql)
    return results


def get_all_tasks_by_course_teacher(teacher_id):
    """Get all course data from the database"""
    sql = """
        select
        t."id", t.task_description,
        t.task_name, t.task_score, t.task_type,
        t.task_due_date, t.year_course_reln_id,
        cyn.academic_year, c.subject, c.course_name, cyn.room_number, u.first_name || ' ' || u.last_name as teacher_name
        from student_incentive_plan.task t 
        inner join student_incentive_plan.course_year_reln cyn on t.year_course_reln_id = cyn.id
        inner join student_incentive_plan.course c on c."id" = cyn.course_id
        inner join student_incentive_plan.user u on u."id" = cyn.teacher_id
        where cyn.teacher_id = {}
        order by academic_year, c.subject, c.course_name
    """.format(teacher_id)
    results = pg_db_conn.execute_query(sql)
    return results

def insert_task(year_course_reln_id, task_name, task_type, task_description, task_due_date,
                task_score):
    """Insert a new course into the database"""
    sql = """
        insert into student_incentive_plan.task (id, year_course_reln_id, task_name, task_type, task_description, task_due_date, task_score)
        values (%s, %s, '%s', '%s', '%s', '%s', %s)
    """
    params = (
        utils.get_unique_id(), year_course_reln_id, task_name, task_type, task_description, task_due_date, task_score)
    ret_sts = pg_db_conn.execute_insert(sql, params)
    return ret_sts


def get_all_tasks_by_student(user_id:int):
    """Get all course data from the database"""
    sql = """
    select
        student.first_name || ' ' || student.last_name as student_name, t."id", t.task_description,
        t.task_name, t.task_score, t.task_type,
        t.task_due_date, t.year_course_reln_id,
        cyr.academic_year,
        c.subject, c.course_name, cyr.room_number, u.first_name || ' ' || u.last_name as teacher_name,
        us.id as schedule_id, us.start_date, us.end_date, us.completion_percentage, us.status, us."update"
    from student_incentive_plan.task t
        inner join student_incentive_plan.course_year_reln cyr on t.year_course_reln_id = cyr.id
        inner join student_incentive_plan.course c on c."id" = cyr.course_id
        inner join student_incentive_plan.user u on u."id" = cyr.teacher_id
        inner join student_incentive_plan.user_course_reln ucr on ucr.year_course_reln_id = cyr."id"
        inner join student_incentive_plan.user student on student.id = ucr.user_id
        left outer join student_incentive_plan.user_schedule us on us.user_id = student.id and us.task_id = t.id
    where student.id = {}
    order by student_name, academic_year, c.subject, c.course_name, t.task_due_date, t.task_type, t.task_name
    """.format(user_id)
    results = pg_db_conn.execute_query(sql)
    return results


def get_task_by_id(task_id):
    """Get all course data from the database"""
    sql = """
    select
        t."id", t.task_description,
        t.task_name, t.task_score, t.task_type,
        t.task_due_date, t.year_course_reln_id,
        cyn.academic_year, c.subject, c.course_name, cyn.room_number, u.first_name || ' ' || u.last_name as teacher_name
    from student_incentive_plan.task t 
        inner join student_incentive_plan.course_year_reln cyn on t.year_course_reln_id = cyn.id
        inner join student_incentive_plan.course c on c."id" = cyn.course_id
        inner join student_incentive_plan.user u on u."id" = cyn.teacher_id
    where t.id = {}
    """.format(task_id)
    results = pg_db_conn.execute_query(sql)
    return results