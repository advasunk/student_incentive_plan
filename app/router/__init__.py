from starlette.templating import Jinja2Templates
from app.__init__ import templates as templates_from_main
# templates = Jinja2Templates(directory="templates")

templates = templates_from_main