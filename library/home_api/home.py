from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles
import os

home_router = APIRouter(tags=["Home"])
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

####### Serve robots.txt ######
@home_router.get("/robots.txt", responses={200: {"description": "Success"}, 404: {"description": "Not Found"}})
def robots():
    """
        Serves robots.txt
    """
    if os.path.exists(os.path.join(static_path,"static/robots.txt")):
        return FileResponse(os.path.join(static_path,"static/robots.txt"))
    else:
        return ORJSONResponse(content={"error": "File not found"}, status_code=404)

####### Serve favicon #######
@home_router.get("/favicon.ico", responses={200: {"description": "Success"}, 404: {"description": "Not Found"}})
def favicon():
    """
        Serves the favicon
    """
    if os.path.exists(os.path.join(static_path,"static/favicon.ico")):
        return FileResponse(os.path.join(static_path,"static/favicon.ico"))
    else:
        return ORJSONResponse(content={"error": "File not found"}, status_code=404)


####### Serve static files + React Build #######
@home_router.get("/")
@home_router.get("/{path:path}", responses={200: {"description": "Success"}, 404: {"description": "Not Found"}})
def home(request: Request, path: str=None):
    """
        Serves the React Build
    """ 
    static_file_path = os.path.join(static_path, path)
    
    ## Return Static Files for React Build
    # Check if static file is a js or css file (Otherwise, it can leak uploads and exports)
    if static_file_path.endswith(".js") or static_file_path.endswith(".css") or static_file_path.endswith(".svg"):
        # Checks if Static file exists
        if os.path.isfile(static_file_path):
            return FileResponse(static_file_path)    
    
    # Check if react build exists
    if os.path.exists(os.path.join(static_path, "templates/index.html")):
        return HTMLResponse(open(os.path.join(static_path, "templates/index.html"), "r").read())
    return ORJSONResponse(content={"error": "React Build not found"}, status_code=404)