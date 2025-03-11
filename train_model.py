import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import shutil

# ---------------------------
# Optional: Extra Augmentation for Minority Class
# ---------------------------
def augment_minority_class(input_folder, output_folder, num_augmented=5, target_size=(150,150)):
    """
    Augments images from the minority class folder and saves augmented copies.
    
    Args:
        input_folder (str): Path to the original images (minority class).
        output_folder (str): Folder where augmented images will be saved.
        num_augmented (int): Number of augmented images to generate per original image.
        target_size (tuple): Size to which images are resized.
    """
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    
    # Define a separate data generator for extra augmentation
    aug_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.15,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process each image in the input folder
    for img_name in os.listdir(input_folder):
        img_path = os.path.join(input_folder, img_name)
        # Load and preprocess the image
        image = load_img(img_path, target_size=target_size)
        x = img_to_array(image)
        x = np.expand_dims(x, axis=0)  # shape (1, height, width, channels)
        
        i = 0
        # Generate augmented images and save them
        for batch in aug_datagen.flow(x, batch_size=1, save_to_dir=output_folder, 
                                      save_prefix='aug', save_format='jpeg'):
            i += 1
            if i >= num_augmented:
                break

# ---------------------------
# Setup for Augmentation
# ---------------------------
# Adjust these paths as needed based on your directory structure and folder names (in caps)
minority_input = "dataset/train/NORMAL"              # original NORMAL images folder
minority_augmented = "dataset/train/NORMAL_augmented"  # folder to save extra augmented images

# Copy original images to the augmented folder so both originals and augmented images are used
if not os.path.exists(minority_augmented):
    os.makedirs(minority_augmented)
for file_name in os.listdir(minority_input):
    shutil.copy(os.path.join(minority_input, file_name), minority_augmented)

# Generate extra augmented images for the minority class
augment_minority_class(minority_input, minority_augmented, num_augmented=3)

# Merge the augmented images back into the NORMAL folder
if os.path.exists(minority_augmented):
    for file_name in os.listdir(minority_augmented):
        source_file = os.path.join(minority_augmented, file_name)
        target_file = os.path.join(minority_input, file_name)
        if os.path.exists(target_file):
            base, ext = os.path.splitext(file_name)
            counter = 1
            new_file_name = f"{base}_dup{counter}{ext}"
            target_file = os.path.join(minority_input, new_file_name)
            while os.path.exists(target_file):
                counter += 1
                new_file_name = f"{base}_dup{counter}{ext}"
                target_file = os.path.join(minority_input, new_file_name)
        shutil.move(source_file, target_file)
    os.rmdir(minority_augmented)
    print("Merged augmented images into NORMAL folder and removed NORMAL_augmented.")

# ---------------------------
# 1. Set Paths to Your Dataset
# ---------------------------
TRAIN_DIR = "dataset/train"
VAL_DIR   = "dataset/val"
TEST_DIR  = "dataset/test"

# ---------------------------
# 2. Hyperparameters
# ---------------------------
IMG_WIDTH, IMG_HEIGHT = 150, 150
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001

# ---------------------------
# 3. Data Augmentation and Generators
# ---------------------------
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)
val_datagen = ImageDataGenerator(rescale=1./255)

# ---------------------------
# 4. Create Generators
# ---------------------------
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)
val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# ---------------------------
# 5. Define the CNN Model
# ---------------------------
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    MaxPooling2D(pool_size=(2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(pool_size=(2,2)),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(pool_size=(2,2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

# ---------------------------
# 6. Compile the Model
# ---------------------------
model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=LEARNING_RATE),
    metrics=['accuracy']
)

# ---------------------------
# 7. Train the Model
# ---------------------------
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator
)

# ---------------------------
# 8. Evaluate on the Test Set (Optional)
# ---------------------------
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

test_loss, test_acc = model.evaluate(test_generator)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_acc)

# ---------------------------
# 9. Save the Model
# ---------------------------
model.save("pneumonia_detector.h5")
print("Model saved as pneumonia_detector.h5")
