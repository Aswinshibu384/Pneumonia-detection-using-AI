import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Load the trained model
model = load_model("pneumonia_detector.h5")

# Path to the test image (update this with the correct path)
import os
image_path = os.path.join(os.getcwd(), "dataset", "test", "PNEUMONIA", "download.jpeg")


# Load the image in RGB format (ensure 3 channels)
try:
    image = load_img(image_path, target_size=(150, 150))  # Ensure correct size
    image = img_to_array(image)  # Convert to array
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize pixel values
    
    # Predict
    prediction = model.predict(image)
    
    # Print result
    if prediction[0][0] > 0.5:
        print("Prediction: PNEUMONIA detected")
    else:
        print("Prediction: NORMAL (No Pneumonia)")

except FileNotFoundError:
    print(f"Test image not found at: {image_path}")
except Exception as e:
    print(f"Error occurred: {e}")
