import tensorflow as tf

def predict(img, path):
    model =  tf.saved_model.load(f"{path}/aiy_vision_classifier_birds_V1_1")
    infer = model.signatures["image_classifier"]

    # Make a prediction
    output = infer(tf.constant(img))

    # Get the output values    
    logits = output['logits']

    # Get the predicted class labels
    top_values, top_indices = tf.math.top_k(logits, k=102)

    # Convert the tensors to Python lists
    top_values = top_values.numpy().tolist()[0]
    top_indices = top_indices.numpy().tolist()[0]

    with open(f"{path}/labels.txt", 'r') as file:
        lines = file.readlines()
    labels = [line.strip() for line in lines]

    # Keep only top 100
    values, val_labels = [], []
    for value, index in zip(top_values, top_indices):
        if len(values) < 100:
            values.append(value)
            val_labels.append(labels[index])

    # Pair the top values with their labels
    predictions_list = [[f'{prob:.20f}', label] for prob, label in zip(values, val_labels)]

    return predictions_list