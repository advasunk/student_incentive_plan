from config import pg_db_conn as pg_db_conn
from utils import utils


def get_all_related_users(user_id: int):
    sql = """
        select reln.*,
        pri_usr.first_name || ' ' || pri_usr.last_name as primary_user_name, pri_usr.email as primary_user_email,
        reln_usr.first_name || ' ' || reln_usr.last_name as related_user_name, reln_usr.email as related_user_email
        from student_incentive_plan."user_reln" reln
        inner join student_incentive_plan.user pri_usr on reln.primary_user_id = pri_usr.id
        inner join student_incentive_plan.user reln_usr on reln.related_user_id = reln_usr.id
        and primary_user_id = {}
        order by id, reln_usr.first_name, reln_usr.last_name
        """.format(user_id)
    results = pg_db_conn.execute_query(sql)

    return results


def insert_user_reln(curr_user_id, user_reln_id, relationship):
    """Insert course data into the database"""
    sql = "INSERT INTO student_incentive_plan.user_reln (id, primary_user_id, related_user_id, reln_type, status) " \
          "VALUES ({}, {}, {}, '{}', '{}')".format(
        utils.get_unique_id(), curr_user_id, user_reln_id, relationship, 'Y')
    return pg_db_conn.save_query(sql)


def delete_user_reln(curr_user_id, user_reln_id):
    """Insert course data into the database"""
    sql = "DELETE FROM student_incentive_plan.user_reln WHERE primary_user_id = {} and related_user_id = {}".format(
        curr_user_id, user_reln_id)
    return pg_db_conn.save_query(sql)