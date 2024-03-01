## Model Formats Specification v1
Each model should have its own folder named after its model (The folder name is publicly visible).  
A basic folder should contain the following files in its root directory:

- `preprocess.py`
- `predict.py`
- `metadata.txt`

Note: The specific model's folder structure can deviate from this structure, but these files must be present in the root directory.

The requirements and guidelines for each file are as follows:

### preprocess.py
Each preprocess.py file must contain a function named `preprocess_image` that takes in an image path and returns a preprocessed image for the model.

#### Limitations
- The function **MUST** not change the image stored at the image path.
- The function is only expected to handle a single image at a time.  
- The function is expected to handle image inputs for all of the following image formats [.png, .jpg, .jpeg, .gif]
- The function is not expected to handle the case where the image path is invalid. 
    - The backend is expected to only pass valid image paths to the function.


##### Example preprocess.py file:
```python
def preprocess_image(image_path):
    # Preprocess image
    return image
```

#### Notes
The preprocess file does not have to follow most of the guidelines for the predict file.
- An example is to have the function pass the `image_path` along if the model does not require preprocessing.  

The only hard requirements are as follows:
- The file must have a function is named `preprocess_image` that takes an `image_path` argument and returns an object.
- The file must not change the image stored at the image path.

### predict.py
Each predict.py file must contain a function named `predict` that takes in both a preprocessed image, its root folder path and returns a prediction for the model.

#### Limitations
- The function is only expected to handle a single image at a time.
- The function is expected to return a prediction for the image.

##### Example predict.py file:
```python
from keras.models import load_model

def predict(img, path):
    model = load_model(f"{path}\model.h5")
    return model.predict(img)
```
### Predict() Function Return format
You are expected to handle labelling in `predict.py`/
- The required format is a sorted list of predictions with the highest probability first.
- Format: [probabilityString(20 d.p. or less), label]
- Example: 
    ```
        [['0.99999999999999999999', 'cat'], ['0.00000000000000000001', 'dog']]
    ```

#### Notes
The `predict.py` function requirements are quite loose.  

### metadata.txt
The metadata.txt file is a text file that contains information about the model so the backend can handle different models.

#### Limitations
- The properties are not case sensitive.
- The properties **ARE** case sensitive.

#### Fields (In Order)
- Model Format Specification Version
- Predict.py return type (integration or loose)
- Model Framework

##### Example metadata.txt file:
```txt
v2
integrated
tensorflow
```

#### Field Descriptions
- Model Format Specification Version\
The version of the model format specification that the model follows.
    - The current version is `v2`,
    - `v1` represents the lack of a specification and is non-functional.
- Predict.py return type\
  The type of return that the predict.py file returns.
    - `integrated` means that the predict.py file handles labelling and returns a formatted prediction.
    - `loose` means that the predict.py file returns a list of probabilities in label order.
        - This requires a `label.txt` file to be present in the model folder.
- Model Framework\
The framework that the model uses.
    - Current options: [`tensorflow` and `pytorch`]
    - This property is not currently used by the backend, but is included for future use.
