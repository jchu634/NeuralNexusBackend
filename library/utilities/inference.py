import imp

from ..config import Settings

current_model = "general_insects"
path = Settings.MODEL_FOLDER
isProduction = Settings.ENV_TYPE == 'production'

metadata_cache = {}
keys = ["specVersion", "mlFramework", "fileTypes"]

def get_labels(model_name="general_insects"):
    filename = f'{path}/{model_name}/labels.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()
    labels = [line.strip() for line in lines]
    return labels

def get_metadata(model_name):
    # Check if the metadata is already in the cache
    if model_name in metadata_cache:
        return metadata_cache[model_name]
    
    filename = f'{path}/{model_name}/metadata.txt'
    metadata = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

    for key, line in zip(keys, lines):
        metadata[key] = line.strip().lower()

    metadata["fileTypes"] = metadata["fileTypes"].upper().strip().split(",")
    metadata_cache[model_name] = metadata

    return metadata

                 
def get_prediction(image_path, current_model):
    metadata = get_metadata(current_model)

    # Preprocess the image
    preprocess = imp.load_source('img_preprocess', f'{path}/{current_model}/preprocess.py')
    img = preprocess.img_preprocess(image_path)
    
    # Get the prediction from the model
    predict = imp.load_source('predict', f'{path}/{current_model}/predict.py')
    prediction = predict.predict(img, f'{path}/{current_model}')

    return prediction
    
