import time

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from __init__ import templates
from auth import session_manager
from auth.session_manager_router import session_manager_router as session_manager_router
from router.course_router import api as course_router
from router.course_year_router import api as academic_year_course_reln_router
from router.html_router import api as html_router
from router.login_router import auth_router
from router.student_course_router import api as user_course_router
from router.student_task_router import api as student_task_router
from router.task_router import api as task_router
from router.user_router import api as user_router
from router.user_reln_router import api as user_reln_router
from router.user_schedule_router import api as user_schedule_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

[app.include_router(api_route) for api_route in [
    auth_router, session_manager_router,
    html_router, user_router, course_router, academic_year_course_reln_router,
    user_course_router, task_router, student_task_router,
    user_reln_router, user_schedule_router
]]


# command to start the server
# uvicorn main:app --reload
# main is the file name, app is the name of our app variable
# and — reload will restart our server anytime we make a change to the code
# and should only be used in development.

def configure_static(app: FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    # rediret to /hello
    response = RedirectResponse(url='/login')
    return response


@app.get("/hello")
def read_hello():
    return {"Hello": "World"}


async def append_session_data_to_response(response, session_data):
    response_body = ""
    for chunk in response.body_iterator:
        response_body += chunk
    # print(f"response_body={response_body}")
    return Response(content=response_body, status_code=response.status_code,
                    headers=dict(response.headers), media_type=response.media_type)


@app.middleware("http")
async def validate_user_session(request: Request, call_next):
    # print the request url
    req_url = str(request.url)
    # print('middleware request.url: ', req_url)
    # print request method
    req_method = str(request.method)
    # print(req_method)
    # if req_url containts /login, then continue with the request, else check for session data

    start_time = time.time()
    # print('middleware starttime: ', start_time)
    if req_url.find('/static/') and req_method == 'GET':
        response = await call_next(request)
        return response
    elif req_url.find('/login') and req_method == 'POST':
        # request is from login page, so continue with the request
        response = await call_next(request)
        process_time = time.time() - start_time
        # print('middleware process_time: ', process_time)
        response.headers["X-Process-Time"] = str(process_time)
        return response
    else:
        # get session data from request. If session data is not available, then redirect to login page, else continue with home page
        session_data = session_manager.get_session_data(request)
        # convert json to SessionData object
        session_data = session_manager.convert_json_to_session_data(session_data)
        # print('session_data: ', session_data)
        if session_data is None or session_data == '' or session_data == {} or session_data['user_id'] is None or \
                session_data['user_id'] == '' or session_data['user_id'] == {}:
            return templates.TemplateResponse("login.html", {"request": request})
        else:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)

            # user is logged in - get the session data and attach as params to the response
            response.headers["session_data"] = str(session_data)

            request.headers.__dict__["_list"].append(
                (
                    'session_data', session_data
                )
            )
            return response
    #


app.add_middleware(SessionMiddleware, secret_key="some-random-string")

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
