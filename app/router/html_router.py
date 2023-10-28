from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi.responses import HTMLResponse

from __init__ import templates
from auth import session_manager
from utils import utils

api = APIRouter(tags=['web api'], prefix="/h")

'''
https://www.starlette.io/requests/

Query Parameters
Query parameters are exposed as an immutable multi-dict.

For example: request.query_params['search']

Path Parameters
Router path parameters are exposed as a dictionary interface.

For example: request.path_params['username']
'''


@api.get("", status_code=200, response_class=HTMLResponse)
# @api.get("", status_code=200, response_model=CourseFindManyItemListResponseModel)
async def direct_request(request: Request):
    print(request.client.host)
    # get session data from request. If session data is not available, then redirect to login page, else continue with home page
    session_data = session_manager.get_session_data(request)
    if session_data is None:
        # redirect response to /login page
        return templates.TemplateResponse("login.html", {"request": request})
    else:
        data_dict = utils.build_data_dict(None, '', '', 'home')
        return templates.TemplateResponse("home.html", {"request": request, 'data_dict': data_dict})


@api.get("/home.html", status_code=200, response_class=HTMLResponse)
# @api.get("", status_code=200, response_model=CourseFindManyItemListResponseModel)
async def process_request_to_home(request: Request):
    # return templates.TemplateResponse("home.html", {"request": request})
    return direct_request(request)


@api.post("/config", status_code=200, response_class=HTMLResponse)
async def process_request_to_config(request: Request, academic_year: str = Form(...)):
    session_manager.save_data_to_session(request, 'academic_year', academic_year)

    data_dict = utils.build_data_dict(None, 'Configurations saved successfully', '', 'home')
    data_dict['academic_year'] = academic_year

    return templates.TemplateResponse("home.html", {"request": request, 'data_dict': data_dict})
