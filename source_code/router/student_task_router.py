from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from __init__ import templates
from auth import session_manager
from dao import task_dao
from utils import utils

api = APIRouter(tags=['course api'], prefix="/student_task")


@api.get("", status_code=200, response_class=HTMLResponse)
async def get_all_tasks(request: Request):
    # get parameter from request
    # user_role = utils.get_request_attribute(request, 'r')
    # user_id = utils.get_request_attribute(request, 'id')
    user_id = session_manager.get_session_data_attrib(request, 'user_id')

    # get all courses from database
    data = task_dao.get_all_tasks_by_student(user_id)
    # set status to 'A' if it is '' or null
    # data['status'] = data['status'].apply(lambda schedule_sts: 'A' if schedule_sts == '' or schedule_sts is None else schedule_sts)

    return templates.TemplateResponse("student_task_list.html",
                                      {"request": request, "data": utils.convert_dataframe_to_dict(data)})
