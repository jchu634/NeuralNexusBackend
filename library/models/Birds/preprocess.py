import tensorflow as tf

def img_preprocess(image_path):    
    # Load the image file and resize it to 224 x 224 pixels
    img = tf.keras.utils.load_img(image_path, target_size=[224, 224])
    
    # Convert the image to an array
    x = tf.keras.utils.img_to_array(img)

    # Scale the pixel values to [0, 1]
    x = x / 255.0

    # Add a batch dimension
    x = tf.expand_dims(x, axis=0)

    # Preprocess the array for MobileNet
    # x = tf.keras.applications.mobilenet.preprocess_input(x[tf.newaxis,...])

    return x