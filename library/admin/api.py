import io
from fastapi import APIRouter, HTTPException, status, Depends, Security, status
from fastapi.responses import ORJSONResponse, JSONResponse, FileResponse, Response

from library.utilities.utilities import clear_cache
from library.database.database import SessionLocal
from library.auth.api import check_if_user_admin, credentials_exception
from library.config import Settings

from typing import Annotated
import traceback
import logging

################ Blueprint/Namespace Configuration ################
admin_api = APIRouter(tags=["Admin"], prefix="/api/v1/admin")

################ Global Variables ################
img_path = Settings.UPLOAD_FOLDER
models_path = Settings.MODEL_FOLDER
isProduction = Settings.ENV_TYPE == 'production'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

################ API Endpoints ################


@admin_api.get('/clear_inference_cache', responses={200: {"description": "Success"}, 500: {"description": "Internal Server Error"}})
def clear_inference_cache(is_admin: Annotated[bool, Security(check_if_user_admin, scopes=["admin"])]):
    """
     Clears the inference cache
    """
    if not is_admin:
        raise credentials_exception
    try:
        clear_cache()
        return JSONResponse(content={"success": "cache cleared"})
    except Exception as e:
        logging.error(f"Cache clear error: {traceback.format_exc()}")
        return ORJSONResponse(content={"error": "Internal Server Error"}, status_code=500)


@admin_api.get('/get_log')
def get_file_logs(is_admin: Annotated[bool, Security(check_if_user_admin, scopes=["admin"])]):
    """
        Returns the server logs
    """
    if not is_admin:
        raise credentials_exception
    try:

        # Note: Cannot utilise FileResponse, as FileResponse will raise an exception
        # This request creates a log, which causes a desync with file size which causes an exception: "Too much data for declared Content-Length"
        logging.info("Exporting Server Logs")
        with open("logfile.log", "rb") as f:
            mem = io.BytesIO(f.read())
        headers = {
            "Content-Disposition": 'attachment; filename="logfile.log"',
        }
        return Response(content=mem.getvalue(), media_type="application/octet-stream", headers=headers)
    except Exception as e:
        logging.error(f"LogFile error: {traceback.format_exc()}")
        return ORJSONResponse(content={"error": "Internal Server Error"}, status_code=500)
