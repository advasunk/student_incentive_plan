import pandas as pd

from config import pg_db_conn as pg_db_conn
from utils import utils


def get_all_courses_year_list():
    """Get all course data from the database"""
    sql = """    
        select c.subject, c.course_name, aycr.room_number, first_name || ' ' || last_name as teacher_name, aycr.*
        from student_incentive_plan.course_year_reln aycr
        inner join student_incentive_plan.course c on aycr.course_id = c.id
        inner join student_incentive_plan.user teacher on teacher.id = aycr.teacher_id
        """
    results = pg_db_conn.execute_query(sql)
    return results


def get_all_courses_year_list_by_teacher_id(teacher_id):
    """Get all course data from the database"""
    sql = """    
        select c.subject, c.course_name, aycr.room_number, first_name || ' ' || last_name as teacher_name, aycr.*
        from student_incentive_plan.course_year_reln aycr
        inner join student_incentive_plan.course c on aycr.course_id = c.id
        inner join student_incentive_plan.user teacher on teacher.id = aycr.teacher_id
        where teacher.id = {}
        order by academic_year, c.subject, c.course_name, teacher.first_name, teacher.last_name
        """.format(teacher_id)

    results = pg_db_conn.execute_query(sql)
    return results

def get_course_year_data_by_id(course_id):
    """Get course data from the database by course id"""
    sql = """    
        select c.subject, c.course_name, aycr.room_number, first_name || ' ' || last_name as teacher_name, aycr.*
        from student_incentive_plan.course_year_reln aycr
        inner join student_incentive_plan.course c on aycr.course_id = c.id
        inner join student_incentive_plan.user teacher on teacher.id = aycr.teacher_id
        where course.id = {}
        order by academic_year, c.subject, c.course_name, teacher.first_name, teacher.last_name
        """.format(course_id)
    results = pg_db_conn.execute_query(sql)
    return results


def get_course_data_by_year_and_course_id(year, course_id):
    sql = """    
        select c.subject, c.course_name, aycr.room_number, first_name || ' ' || last_name as teacher_name, aycr.*
        from student_incentive_plan.course_year_reln aycr
        inner join student_incentive_plan.course c on aycr.course_id = c.id
        inner join student_incentive_plan.user teacher on teacher.id = aycr.teacher_id
        where academic_year = '{}' and course_id = {}
        order by academic_year, c.subject, c.course_name, teacher.first_name, teacher.last_name
        """.format(year, course_id)

    results = pg_db_conn.execute_query(sql)
    return results


def get_course_data_by_year(academic_year):
    sql = """
        select c.subject, c.course_name, teacher.first_name, teacher.last_name, 
        teacher.first_name || ' ' || teacher.last_name as teacher_name, aycr.*
        from student_incentive_plan.course_year_reln aycr
        inner join student_incentive_plan.course c on aycr.course_id = c.id
        inner join student_incentive_plan.user teacher on teacher.id = aycr.teacher_id
        where aycr.academic_year = '{}' 
        order by academic_year, c.subject, c.course_name, teacher.first_name, teacher.last_name
        """.format(academic_year)
    results = pg_db_conn.execute_query(sql)
    return results


if __name__ == "__main__":
    df = get_all_courses_year_list()
    print(df)


def insert_course_year_data(academic_year, course_id, room_number, teacher_id):
    """Insert course data into the database"""
    # check if course already exists
    df = get_course_data_by_year_and_course_id(academic_year, course_id)
    if len(df) > 0:
        # course already exists - raise an exception
        raise Exception("Course is already assigned to an Acadamic year")
    else:
        # course does not exist
        pg_db_conn.save_query(
            "INSERT INTO student_incentive_plan.course_year_reln (id, academic_year, course_id, room_number, teacher_id) "
            "VALUES ({}, {}, {}, {}, {})".format(
                utils.get_unique_id(), academic_year, course_id, room_number, teacher_id))
        return True

