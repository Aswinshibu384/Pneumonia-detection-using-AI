import os
import random
import shutil

def create_val_split(train_class_path, val_class_path, val_ratio=0.2):
    """
    Moves a percentage of images from the train directory to the validation directory.

    Args:
        train_class_path (str): Path to the training images for a given class.
        val_class_path (str): Path to where the validation images should be moved.
        val_ratio (float): The fraction of images to move to validation.
    """
    # Create validation directory if it doesn't exist
    if not os.path.exists(val_class_path):
        os.makedirs(val_class_path)
    
    # List all files in the train folder
    all_images = os.listdir(train_class_path)
    random.shuffle(all_images)
    
    # Calculate the number of images to move
    val_count = int(len(all_images) * val_ratio)
    
    # Move the selected images to the validation folder
    for i in range(val_count):
        img = all_images[i]
        src = os.path.join(train_class_path, img)
        dst = os.path.join(val_class_path, img)
        shutil.move(src, dst)
        print(f"Moved {img} from {train_class_path} to {val_class_path}")

# Example usage:
# Adjust the paths as per your folder structure
# For the NORMAL class:
create_val_split("dataset/train/NORMAL", "dataset/val/NORMAL", val_ratio=0.2)
# For the PNEUMONIA class:
create_val_split("dataset/train/PNEUMONIA", "dataset/val/PNEUMONIA", val_ratio=0.2)
