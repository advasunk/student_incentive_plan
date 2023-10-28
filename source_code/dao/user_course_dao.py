import pandas as pd

from config import pg_db_conn as pg_db_conn
from utils import utils


def get_all_user_courses():
    """Get all course data from the database"""
    sql = ("""select user_course_reln.*, usr.first_name || ' ' || usr.last_name as student_name,
           teacher.first_name || ' ' || teacher.last_name as teacher_name, teacher.id as teacher_id,
           course.course_name, course.subject, course.id as course_id, course_year_reln.academic_year,
           course_year_reln.room_number
           from student_incentive_plan.user_course_reln user_course_reln
           left outer join student_incentive_plan.user usr on user_course_reln.user_id = usr.id
           left outer join student_incentive_plan.course_year_reln course_year_reln on user_course_reln.year_course_reln_id = course_year_reln.id
           left outer join student_incentive_plan.course course on course.id = course_year_reln.course_id
           left outer join student_incentive_plan.user teacher on course_year_reln.teacher_id = teacher.id
           order by usr.first_name, usr.last_name, course_year_reln.academic_year, course.subject, course.course_name
           """)
    results = pg_db_conn.execute_query(sql)
    return results


def get_user_courses_by_user_id(user_id:int):
    """Get all course data from the database"""
    sql = ("""select user_course_reln.*, usr.first_name || ' ' || usr.last_name as student_name,
           teacher.first_name || ' ' || teacher.last_name as teacher_name, teacher.id as teacher_id,
           course.course_name, course.subject, course.id as course_id, course_year_reln.academic_year,
           course_year_reln.room_number
           from student_incentive_plan.user_course_reln user_course_reln
           left outer join student_incentive_plan.user usr on user_course_reln.user_id = usr.id
           left outer join student_incentive_plan.course_year_reln course_year_reln on user_course_reln.year_course_reln_id = course_year_reln.id
           left outer join student_incentive_plan.course course on course.id = course_year_reln.course_id
           left outer join student_incentive_plan.user teacher on course_year_reln.teacher_id = teacher.id
           where user_course_reln.user_id = {}
           order by usr.first_name, usr.last_name, course_year_reln.academic_year, course.subject, course.course_name
           """.format(user_id))
    results = pg_db_conn.execute_query(sql)
    return results



if __name__ == "__main__":
    df = get_all_user_courses()
    print(df)


def get_user_course_data_by_user_id_and_year_course_reln_id(user_id, year_course_reln_id):
    """Get course data from the database by course id"""
    results = pg_db_conn.execute_query("SELECT * FROM student_incentive_plan.user_course_reln "
                                       "WHERE user_id = {} and year_course_reln_id = {}"
                                       .format(user_id, year_course_reln_id))
    return results


def insert_user_course(user_id, year_course_reln_id):
    """Insert course data into the database"""
    # check if course already exists
    df = get_user_course_data_by_user_id_and_year_course_reln_id(user_id, year_course_reln_id)
    if len(df) > 0:
        # course already exists - raise an exception
        raise Exception("User is already enrolled in the course")
    else:
        # course does not exist
        pg_db_conn.save_query(
            "INSERT INTO student_incentive_plan.user_course_reln (id, user_id, year_course_reln_id) "
            "VALUES ({}, {}, {})".format(
                utils.get_unique_id(), user_id, year_course_reln_id))
        return True


def get_user_courses_by_teacher_id(teacher_id:int):
    """Get all course data from the database"""
    sql = ("""select user_course_reln.*, usr.first_name || ' ' || usr.last_name as student_name,
           teacher.first_name || ' ' || teacher.last_name as teacher_name, teacher.id as teacher_id,
           course.course_name, course.subject, course.id as course_id, course_year_reln.academic_year,
           course_year_reln.room_number
           from student_incentive_plan.user_course_reln user_course_reln
           left outer join student_incentive_plan.user usr on user_course_reln.user_id = usr.id
           left outer join student_incentive_plan.course_year_reln course_year_reln on user_course_reln.year_course_reln_id = course_year_reln.id
           left outer join student_incentive_plan.course course on course.id = course_year_reln.course_id
           left outer join student_incentive_plan.user teacher on course_year_reln.teacher_id = teacher.id
           where course_year_reln.teacher_id = {}
           order by usr.first_name, usr.last_name, course_year_reln.academic_year, course.subject, course.course_name
           """.format(teacher_id))
    results = pg_db_conn.execute_query(sql)
    return results