import os
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# Load trained model
model = load_model("models/age_gender_model.keras", compile=False)


def predict_image(image_path):

    # Read image safely
    if not os.path.exists(image_path):
        raise ValueError(f"Image file does not exist: {image_path}")

    try:
        img = Image.open(image_path).convert("RGB")
        img = np.array(img)
    except Exception as e:
        raise ValueError(f"Could not read image: {image_path}") from e

    # Resize to model input size
    img = cv2.resize(img, (128, 128))

    # Normalize
    img = img.astype("float32") / 255.0

    # Add batch dimension
    img = np.expand_dims(img, axis=0)

    # Prediction
    prediction = model.predict(img, verbose=0)

    # Gender prediction
    gender_pred = prediction["gender"]

    male_prob = float(gender_pred[0][0])
    female_prob = 1.0 - male_prob

    print("==============================")
    print("MALE PROBABILITY:", male_prob)
    print("FEMALE PROBABILITY:", female_prob)
    print("==============================")

    if male_prob >= 0.68:
        gender = "Male"
    else:
        gender = "Female"

    # Age prediction
    age_pred = prediction["age"]
    age = int(round(float(age_pred[0][0])))

    # Keep age within reasonable range
    age = max(0, min(age, 100))

    return age, gender