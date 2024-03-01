from fastapi import APIRouter, UploadFile, Query, WebSocket
from fastapi.responses import ORJSONResponse, JSONResponse, FileResponse
from werkzeug.utils import secure_filename
import mmh3
import shutil
import logging

import sys, os
from ..config import Settings

from library.utilities.inference import get_prediction, get_metadata
import time
import traceback

################ Blueprint/Namespace Configuration ################
utils_api = APIRouter(tags=["Utilities"])

################ Global Variables ################
img_path = Settings.UPLOAD_FOLDER
models_path = Settings.MODEL_FOLDER
isProduction = Settings.ENV_TYPE == 'production'

inference_cache = {}

################ Helper Functions ################
def clear_cache():
    inference_cache.clear()

def is_file_allowed(filename, model=None):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if model:
        return ext.upper() in get_metadata(model)["fileTypes"]
    else:
        return ext.upper() in Settings.ALLOWED_IMAGE_EXTENSIONS

################ API Endpoints ################
@utils_api.post('/api/v1/image_inference', responses={200: {"description": "Success"}, 400: {"description": "Bad Request"}, 405: {"description": "Method Not Allowed"}, 500: {"description": "Internal Server Error"}}, tags=["Utilities"])
# NOTE: currently files does not support documenation:
# Intended documentation: "List of files to upload"
def get_inference(files: list[UploadFile], model: str | None = Query(None, description="Model to use for prediction.")):
    """
     Takes in a list of Image files and returns a list of predictions in JSON format.
    """
    try:
        # Checks if the model is valid before uploading
        if not model or model not in available_models():
            return ORJSONResponse(content={"error": "Invalid Model"}, status_code=400)     
        returnList = []

        for file in files:
            # Check if the file extension is allowed
            if not is_file_allowed(file.filename, model):
                return ORJSONResponse(content={"error": "File type not allowed"}, status_code=405)
            
            # Get the hash of the file
            file.file.seek(0)  # Ensure we're at the start of the file
            hash = mmh3.hash(file.file.read())            

            if (hash, file.filename) in inference_cache and time.time() - inference_cache[(hash, file.filename)]["time"] < Settings.CACHE_TIMEOUT_PERIOD:
                logging.info(f"Inference Cache Hit: Served {hash} ({file.filename})")
                del inference_cache[(hash, file.filename)]["time"]
                returnList.append(inference_cache[(hash, file.filename)])
                inference_cache[(hash, file.filename)]["time"] = time.time()
            else:
                logging.info(f"Inference Cache Miss: Inferered {hash} ({file.filename})")
                file_path = os.path.join(img_path, secure_filename(file.filename))
                file_ext = os.path.splitext(file_path)[1]
                filename_without_ext = os.path.splitext(secure_filename(file.filename))[0]
                file_path = os.path.join(img_path, f"{filename_without_ext}.{str(hash)}{file_ext}")

                # Save the file to disk
                with open(file_path, "wb") as buffer:
                    file.file.seek(0)  # Go back to the start of the file
                    shutil.copyfileobj(file.file, buffer)

                # Get the prediction
                prediction = get_prediction(file_path, model)
                inference_cache[(hash, file.filename)] = {"name": file.filename, "pred": prediction, "hash": hash, "model": model, "time": time.time()}
                returnList.append({"name": file.filename, "pred": prediction, "hash": hash, "model": model})

        return JSONResponse(content=returnList)
    except Exception as e:
        logging.error(f"Inference error: {traceback.format_exc()}")
        return ORJSONResponse(content={"error": "Internal Server Error"}, status_code=500)

def available_models():
    subfolders = [os.path.basename(f.path) for f in os.scandir(models_path) if f.is_dir()]
    return sorted(subfolders, key=str.lower)

@utils_api.get('/api/v1/available_models', tags=["Utilities"])
def get_available_models():
    """
        Returns a list of available models.
    """
    return JSONResponse(content=available_models())

@utils_api.get('/api/v1/model_file_types', tags=["Utilities"])
def get_model_file_types(model_name:str):
    if model_name in available_models():
        return get_metadata(model_name)["fileTypes"]
    else:
        return {"error": "Invalid Model"}

@utils_api.get('/api/v1/get_image', tags=["Utilities"])
def get_image(image_name: str, hash: str):
    """ 
        Returns an image from the uploads folder.
    """
    try:
        filename = secure_filename(image_name)
        file_ext = os.path.splitext(filename)[1]
        filename_without_ext = os.path.splitext(filename)[0]
        filename_with_hash = f"{filename_without_ext}.{hash}{file_ext}"

        filepath = os.path.join(img_path, filename_with_hash)
        
        if not os.path.isfile(filepath) or is_file_allowed(filename) == False:
            return {"error": "File not found"}
        
        return FileResponse(filepath)
    except Exception as e:
        logging.error(f"Image Fetch error: {traceback.format_exc()}")
        return ORJSONResponse(content={"error": "Internal Server Error"}, status_code=500)
        