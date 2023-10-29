from config import pg_db_conn as pg_db_conn
from utils import utils


def get_all_users():
    """Get all course data from the database"""
    results = pg_db_conn.execute_query("SELECT id, first_name, last_name, email, password, "
                                       "date_of_birth, user_type, is_active FROM student_incentive_plan.user")

    return results
    # df = pd.DataFrame(results)
    # df.columns = results[0].keys()
    # # convert the results to a dataframe
    # user_df = pd.DataFrame(results,
    #                   columns=['id', 'first_name', 'last_name', 'email', 'password', 'date_of_birth', 'user_type',
    #                            'is_active'])
    # return user_df


def get_user_by_email(email: None):
    sql_stmt = ("SELECT id, first_name, last_name, email, password, "
                "date_of_birth, user_type, is_active FROM student_incentive_plan.user WHERE email = '" + email + "'")

    # execute_query method returns a dataframe by default
    results = pg_db_conn.execute_query(sql_stmt)

    # if you want to get a list of tuples, set the ret_data_as_df (second parameter) to False
    # this result will not include column headers
    # results2 = pg_db_conn.execute_query(sql_stmt, False)

    return results


if __name__ == "__main__":
    df = get_all_users()
    print(df)


def insert_user(first_name, last_name, email, password, user_type, dob, user_group):
    """Insert course data into the database"""
    sql = "INSERT INTO student_incentive_plan.user (id, first_name, last_name, email, password, date_of_birth, user_type, user_group, is_active) " \
          "VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        utils.get_unique_id(), first_name, last_name, email, password, dob, user_type, user_group, 'Y')
    return pg_db_conn.save_query(sql)


def get_all_users_by_user_type(user_type):
    """Get all course data from the database"""
    results = pg_db_conn.execute_query(
        "SELECT id, first_name, last_name, first_name || ' ' || last_name as student_name, email, "
        "date_of_birth, user_type, is_active FROM student_incentive_plan.user "
        "WHERE upper(user_type) = '{}' order by first_name, last_name".format(user_type.upper()))

    return results


def get_user_data_by_email_and_password(email, password):
    sql_stmt = ("SELECT id, first_name, last_name, email, "
                "date_of_birth, user_type, is_active FROM student_incentive_plan.user "
                "WHERE upper(email) = '" + email.upper() + "' "
                                                           "and upper(password) = '" + password.upper() + "'")
    # execute_query method returns a dataframe by default
    results = pg_db_conn.execute_query(sql_stmt)
    return results


def get_user_by_email_but_not_linked(reln_email, curr_user_id):
    sql = """
        select usr.*
        from student_incentive_plan."user" usr
        where email = '{}'
        and id not in (select related_user_id from student_incentive_plan.user_reln where primary_user_id = {})
        """.format(reln_email, curr_user_id)
    results = pg_db_conn.execute_query(sql)
    return results


def get_user_by_filter(user_type, filter):
    sql = """
        select usr.* from student_incentive_plan."user" usr where true = true
        """
    if user_type:
        sql += " and lower(user_type) = '{}' ".format(user_type)
    if filter:
        sql += " and (lower(first_name) like '%{}%' or lower(last_name) like '%{}%' or lower(email) like '%{}%' )".format(
            filter, filter, filter)

    sql += " order by first_name, last_name"

    results = pg_db_conn.execute_query(sql)
    return results
