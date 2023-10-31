from datetime import timedelta

from fastapi import APIRouter, Request, Form
from starlette.responses import HTMLResponse

from __init__ import templates
from auth import session_manager
from common import platform_data_definitions
from dao import user_schedule_dao, task_dao, user_schedule_assigned_user_reln_dao, user_reln_dao
from utils import utils, date_utility

api = APIRouter(tags=['course api'], prefix="/user_schedule")


@api.get("", status_code=200, response_class=HTMLResponse)
async def get_all_schedules(request: Request):
    # get all schedules from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    data = user_schedule_dao.get_all_schedules_by_user(user_id)

    # replace '&lt;' with '<' and '&gt;' with '>' from data assigned_user_comments
    # data['assigned_user_comments'] = data['assigned_user_comments'].str.replace('&lt;', '<')
    # data['assigned_user_comments'] = data['assigned_user_comments'].str.replace('&gt;', '>')

    data_dict = utils.build_data_dict(data, status_message='', error_message='')
    return templates.TemplateResponse("user_schedule_list.html",
                                      {"request": request, "data_dict": data_dict})


@api.get("/add", status_code=200, response_class=HTMLResponse)
async def show_add_schedule_page(request: Request, task_id: int):
    # get task details from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    task_data = task_dao.get_task_by_id(task_id)

    # add schedule to user_schedule table
    ret_sts = user_schedule_dao.add_schedule_for_task(user_id, utils.convert_dataframe_to_dict(task_data)[0])

    if ret_sts:
        status_message = 'Successfully added schedule for task'
        data = user_schedule_dao.get_all_schedules_by_user(user_id)

        data_dict = utils.build_data_dict(data, status_message=status_message, error_message='')
        # take the user to schedule list page, so they can manage their schedule
        return templates.TemplateResponse("user_schedule_list.html",
                                          {"request": request,
                                           "data_dict": data_dict
                                           })
    else:
        # schedule is not added - take the user back to the task list page
        # send the request to /student_task page
        error_message = 'Failed to add schedule for task'
        data = task_dao.get_all_tasks_by_student(user_id)
        data_dict = utils.build_data_dict(data, status_message='', error_message=error_message)
        return templates.TemplateResponse("student_task_list.html",
                                          {"request": request,
                                           "data_dict": data_dict
                                           })


@api.get("/update", status_code=200, response_class=HTMLResponse)
async def update_schedule(request: Request):
    # get all schedules from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    user_schedule_id = utils.get_request_attribute(request, 'user_schedule_id', '')
    start_date = utils.get_request_attribute(request, 'start_date', '')
    end_date = utils.get_request_attribute(request, 'end_date', '')
    completion_percentage = utils.get_request_attribute(request, 'completion_percentage', '')

    # update user_schedule with new data
    ret_sts = user_schedule_dao.update_user_schedule(user_schedule_id, start_date, end_date, completion_percentage)
    status_message = ''
    error_message = ''
    if ret_sts:
        status_message = 'Successfully updated user schedule'
    else:
        error_message = 'Failed to update user schedule'

    data = user_schedule_dao.get_all_schedules_by_user(user_id)
    data_dict = utils.build_data_dict(data, status_message=status_message, error_message=error_message)
    return templates.TemplateResponse("user_schedule_list.html",
                                      {"request": request, "data_dict": data_dict})


@api.get("/delete", status_code=200, response_class=HTMLResponse)
async def update_schedule(request: Request):
    # get all schedules from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    user_schedule_id = utils.get_request_attribute(request, 'user_schedule_id', '')
    start_date = utils.get_request_attribute(request, 'start_date', '')
    end_date = utils.get_request_attribute(request, 'end_date', '')
    completion_percentage = utils.get_request_attribute(request, 'completion_percentage', '')

    # update user_schedule with new data
    ret_sts = user_schedule_dao.delete_user_schedule(user_schedule_id)
    status_message = ''
    error_message = ''
    if ret_sts:
        status_message = 'Successfully deleted user schedule'
    else:
        error_message = 'Failed to delete user schedule'

    data = user_schedule_dao.get_all_schedules_by_user(user_id)
    data_dict = utils.build_data_dict(data, status_message=status_message, error_message=error_message)
    return templates.TemplateResponse("user_schedule_list.html",
                                      {"request": request, "data_dict": data_dict})


@api.get("/assign/add", status_code=200, response_class=HTMLResponse)
async def user_schedule_assign_add(request: Request):
    # get all schedules from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    user_schedule_id = utils.get_request_attribute(request, 'user_schedule_id', '')

    # get schedule details from database
    user_schedule_data = user_schedule_dao.get_schedule_by_id(user_schedule_id)
    # get linked user details from database
    user_reln_data = user_reln_dao.get_all_related_users(user_id)

    data_dict = utils.build_data_dict(user_schedule_data, status_message='', error_message='',
                                      data_set_name='user_schedule_data')
    data_dict['user_schedule_id'] = user_schedule_id
    data_dict['user_reln_data'] = utils.convert_dataframe_to_dict(user_reln_data)

    return templates.TemplateResponse("user_schedule_assign_add.html",
                                      {"request": request, "data_dict": data_dict})


@api.post("/assign/add", status_code=200, response_class=HTMLResponse)
async def user_schedule_assign_add(request: Request, user_schedule_id: int = Form(...)):
    # get all schedules from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')

    form_data = await request.form()
    # get a list of all attributes from the form
    form_data_list = form_data.__dict__['_list']

    print(type(form_data_list))
    # iterate through the list and print each item
    assigned_user_id_list = []
    for item in form_data_list:
        if (item[0] == 'assigned_user_id'):
            assigned_user_id_list.append(item[1])

    # # convert the form data to a dictionary
    # form_data_dict = form_data.__dict__['_dict']
    # print(type(form_data_dict))
    # # iterate through the dictionary and print each item
    # for item in form_data_dict:
    #     print(item)
    #     print(form_data_dict[item])

    # insert assigned user for task based on the user_schedule_id
    error_message = ''
    for assigned_user_id in assigned_user_id_list:
        ret_sts = user_schedule_assigned_user_reln_dao.add_assigned_user_for_schedule(user_schedule_id,
                                                                                      assigned_user_id,
                                                                                      '')
        if not ret_sts:
            error_message = error_message + 'Failed to add assigned user for schedule {} and user {}'.format(
                user_schedule_id, assigned_user_id)

    if not error_message:
        status_message = 'Successfully added schedule for task'
        user_schedule_assigned_user_reln_data = user_schedule_assigned_user_reln_dao.get_all_schedule_assignments_by_student(
            user_id)

        # data_dict['user_schedule_reln_data'] = utils.convert_dataframe_to_dict(user_schedule_reln_data)
        data_dict = utils.build_data_dict(user_schedule_assigned_user_reln_data, status_message=status_message,
                                          error_message='',
                                          data_set_name='user_schedule_assigned_user_reln_data')
        data_dict['user_schedule_id'] = user_schedule_id
        # take the user to schedule list page, so they can manage their schedule
        return templates.TemplateResponse("user_schedule_assign_list.html",
                                          {"request": request,
                                           "data_dict": data_dict
                                           })
    else:
        # schedule is not added - take the user back to the task list page
        # send the request to /student_task page
        data = user_schedule_dao.get_all_schedules_by_user(user_id)
        data_dict = utils.build_data_dict(data, status_message='', error_message=error_message)
        return templates.TemplateResponse("user_schedule_list.html",
                                          {"request": request, "data_dict": data_dict})


def check_task_due_date_and_schedule_end_date(user_schedules_dict):
    # iterate over the dictionary and convert the string datetime to date
    # for item in user_schedules_dict:
    #     item['start_date'] = date_utility.convert_str_to_date(item['start_date'])
    #     item['task_due_date'] = date_utility.convert_str_to_date(item['task_due_date'])
    #     item['end_date'] = date_utility.convert_str_to_date(item['end_date'])


    # iterate over the dictionary and convert the date to string
    # for item in user_schedules_dict:
    #     item['task_start_date'] = date_utility.format_date_to_string(item['task_start_date'])
    #     item['task_due_date'] = date_utility.format_date_to_string(item['task_due_date'])
    #     item['end_date'] = date_utility.format_date_to_string(item['end_date'])

    user_schedules_dict_updated = []
    # check task due date and schedule end date and set the status if the task is overdue or due with in 2 days
    for row in user_schedules_dict:
        # check if the task is overdue
        if row['task_due_date'] < date_utility.get_current_date_as_date():
            row['status'] = 'Overdue'
        # check if the task is due with in 2 days
        elif row['task_due_date'] <= date_utility.get_current_date_as_date() + timedelta(days=2):
            row['status'] = 'Due in 2 days'
        elif row['task_due_date'] < row['end_date']:
            row['status'] = 'Overdue'
        else:
            row['status'] = ''

        user_schedules_dict_updated.append(row)

    return user_schedules_dict_updated


@api.get("/assign/list", status_code=200, response_class=HTMLResponse)
async def user_schedule_assign_list(request: Request):
    # get all schedules from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')

    data_dict = utils.build_data_dict(None, status_message='', error_message='')

    # add schedules of the student
    user_schedule_assigned_user_reln_data_by_student = (
        user_schedule_assigned_user_reln_dao.get_all_schedule_assignments_by_student(user_id))

    user_schedule_assigned_user_reln_data_by_student = check_task_due_date_and_schedule_end_date(
        utils.convert_dataframe_to_dict(user_schedule_assigned_user_reln_data_by_student))

    data_dict['user_schedule_assigned_user_reln_data_by_student'] = user_schedule_assigned_user_reln_data_by_student

    # add schedules assigned to the logged in user
    user_schedule_assigned_user_reln_data_to_user = (
        user_schedule_assigned_user_reln_dao.get_all_schedule_assignments_to_user(user_id))

    user_schedule_assigned_user_reln_data_to_user = check_task_due_date_and_schedule_end_date(
        utils.convert_dataframe_to_dict(user_schedule_assigned_user_reln_data_to_user))

    data_dict['user_schedule_assigned_user_reln_data_to_user'] = user_schedule_assigned_user_reln_data_to_user

    return templates.TemplateResponse("user_schedule_assign_list.html",
                                      {"request": request, "data_dict": data_dict})


@api.post("/assign/feedback", status_code=200, response_class=HTMLResponse)
async def user_schedule_assign_feedback(request: Request):
    # get all schedules from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    user_name = session_manager.get_session_data_attrib(request, 'user_name')
    # convert user_name (full name) to first name and first letter of last name
    user_name_short = user_name.split(' ')[0] + ' ' + user_name.split(' ')[1][0]

    form_data = await request.form()
    # get a list of all attributes from the form
    form_data_list = form_data.__dict__['_list']

    id = utils.get_form_attribute(form_data_list, 'id', '')
    # user_schedule_id = utils.get_form_attribute(form_data_list, 'user_schedule_id', '')
    # assigned_user_id = utils.get_form_attribute(form_data_list, 'assigned_user_id', '')
    # assigned_user_comments = utils.get_form_attribute(form_data_list, 'assigned_user_comments', '')

    # iterate through the form data list and get the values
    # TODO - Get the values where comments are available and update the database
    """
        Sample form data list:
        ('assigned_user_comments_20231027030539996', '1')
        ('id_20231027030539996', '20231027030539996')
        ('assigned_user_comments_20231027030540012', '2')
        ('id_20231027030540012', '20231027030540012')
        ('submit', '')
    """
    updates = {}
    assigned_user_comments = ''
    for item in form_data_list:
        if str(item[0]).startswith('assigned_user_comments_'):
            user_sched_assigned_id = str(item[0]).replace('assigned_user_comments_', '')
            updates[user_sched_assigned_id] = item[1]

    print(updates)
    status_message = ''
    error_message = ''

    # iterate through the updates dictionary and update the database
    for key, value in updates.items():
        # get current schedule assignment
        user_schedule_assigned_user_reln_curr = user_schedule_assigned_user_reln_dao.get_assigned_schedule_by_id(key)
        curr_schedule_assignment_json = utils.convert_dataframe_to_dict(user_schedule_assigned_user_reln_curr)[0]

        curr_comments = curr_schedule_assignment_json['assigned_user_comments']
        if curr_comments:
            curr_comments = curr_comments + '\n'

        # add date and time to the comments
        assigned_user_comments = curr_comments + (
                'Upd. by: ' + user_name_short + ' at ' + date_utility.format_date_time_to_string().strip() + ':\n' + value)

        # update user_schedule with new data
        ret_sts = user_schedule_assigned_user_reln_dao.update_user_schedule_assign_feedback(key, assigned_user_comments)
        if ret_sts:
            status_message = status_message + '> Successfully updated user schedule assignment feedback for ' + key
        else:
            error_message = error_message + '> Failed to update user schedule assignment feedback for ' + key

    data_dict = utils.build_data_dict(None, status_message=status_message, error_message=error_message)

    # add schedules of the student
    user_schedule_assigned_user_reln_data_by_student = (
        user_schedule_assigned_user_reln_dao.get_all_schedule_assignments_by_student(user_id))
    data_dict['user_schedule_assigned_user_reln_data_by_student'] = utils.convert_dataframe_to_dict(
        user_schedule_assigned_user_reln_data_by_student)

    # add schedules assigned to the logged in user
    user_schedule_assigned_user_reln_data_to_user = (
        user_schedule_assigned_user_reln_dao.get_all_schedule_assignments_to_user(user_id))
    data_dict['user_schedule_assigned_user_reln_data_to_user'] = utils.convert_dataframe_to_dict(
        user_schedule_assigned_user_reln_data_to_user)

    return templates.TemplateResponse("user_schedule_assign_list.html",
                                      {"request": request, "data_dict": data_dict})
