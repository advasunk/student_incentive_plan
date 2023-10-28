import pandas as pd

from config import pg_db_conn as pg_db_conn
from utils import utils


def get_all_courses():
    """Get all course data from the database"""
    sql = """
        select course.*, cyr.academic_year, cyr.room_number, cyr.id as cyr_id,
        teacher.first_name || teacher.last_name as teacher_name, teacher.id as teacher_id
        from student_incentive_plan.course course
        inner join student_incentive_plan.course_year_reln cyr on cyr.course_id = course."id"
        inner join student_incentive_plan.user teacher on cyr.teacher_id = teacher."id"
        order by teacher_name, academic_year, subject, course_name"""
    results = pg_db_conn.execute_query(sql)
    return results


def get_course_data_by_teacher_id(teacher_id):
    """Get course data from the database by course id"""
    sql = """
        select course.*, cyr.academic_year, cyr.room_number, cyr.id as cyr_id,
        teacher.first_name || teacher.last_name as teacher_name, teacher.id as teacher_id
        from student_incentive_plan.course course
        inner join student_incentive_plan.course_year_reln cyr on cyr.course_id = course."id"
        inner join student_incentive_plan.user teacher on cyr.teacher_id = teacher."id"
        where teacher.id = {}
        order by teacher_name, academic_year, subject, course_name""".format(teacher_id)
    results = pg_db_conn.execute_query(sql)
    return results

def get_course_data_by_id(course_id):
    """Get course data from the database by course id"""
    sql = """
        select course.*, cyr.academic_year, cyr.room_number, cyr.id as cyr_id,
        teacher.first_name || teacher.last_name as teacher_name, teacher.id as teacher_id
        from student_incentive_plan.course course
        inner join student_incentive_plan.course_year_reln cyr on cyr.course_id = course."id"
        inner join student_incentive_plan.user teacher on cyr.teacher_id = teacher."id"
        where course.id = {}
        order by teacher_name, academic_year, subject, course_name""".format(course_id)
    results = pg_db_conn.execute_query(sql)
    return results


def get_course_data_by_name(course_name):
    """Get course data from the database by course name"""
    sql = """
        select course.*, cyr.academic_year, cyr.room_number, cyr.id as cyr_id,
        teacher.first_name || teacher.last_name as teacher_name, teacher.id as teacher_id
        from student_incentive_plan.course course
        inner join student_incentive_plan.course_year_reln cyr on cyr.course_id = course."id"
        inner join student_incentive_plan.user teacher on cyr.teacher_id = teacher."id"
        where lower(course.course_name) = '{}'
        order by teacher_name, academic_year, subject, course_name""".format(course_name.lower())
    results = pg_db_conn.execute_query(sql)
    return results


def get_course_data_by_subject(subject):
    """Get course data from the database by subject"""
    sql = """
        select course.*, cyr.academic_year, cyr.room_number, cyr.id as cyr_id,
        teacher.first_name || teacher.last_name as teacher_name, teacher.id as teacher_id
        from student_incentive_plan.course course
        inner join student_incentive_plan.course_year_reln cyr on cyr.course_id = course."id"
        inner join student_incentive_plan.user teacher on cyr.teacher_id = teacher."id"
        where lower(course.subject) = '{}'
        order by teacher_name, academic_year, subject, course_name""".format(subject.lower())
    results = pg_db_conn.execute_query(sql)
    return results


def get_course_data_by_year(academic_year):
    """Get course data from the database by academic_year"""
    sql = """
        select course.*, cyr.academic_year, cyr.room_number, cyr.id as cyr_id,
        teacher.first_name || teacher.last_name as teacher_name, teacher.id as teacher_id
        from student_incentive_plan.course course
        inner join student_incentive_plan.course_year_reln cyr on cyr.course_id = course."id"
        inner join student_incentive_plan.user teacher on cyr.teacher_id = teacher."id"
        where lower(cyr.academic_year) = '{}'
        order by teacher_name, academic_year, subject, course_name""".format(academic_year.lower())
    results = pg_db_conn.execute_query(sql)
    return results


if __name__ == "__main__":
    df = get_all_courses()
    print(df)


def insert_course(course_name, subject, course_description):
    """Insert course data into the database"""
    sql = "INSERT INTO student_incentive_plan.course (id, course_name, subject, course_description) VALUES ({}, '{}', '{}', '{}')".format(
        utils.get_unique_id(), course_name, subject, course_description)
    # print(sql)
    return pg_db_conn.save_query(sql)
