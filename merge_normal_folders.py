import os
import shutil

# Define the source and target directories
source_dir = os.path.join("dataset", "train", "NORMAL_augmented")
target_dir = os.path.join("dataset", "train", "NORMAL")

# Check if source directory exists
if not os.path.exists(source_dir):
    print(f"Source directory '{source_dir}' does not exist.")
else:
    print(f"Merging files from '{source_dir}' into '{target_dir}' ...")
    files_moved = 0
    
    # Loop over each file in the source directory
    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        target_file = os.path.join(target_dir, file_name)
        
        # Only process files (skip subdirectories if any)
        if os.path.isfile(source_file):
            # If a file with the same name exists in the target, rename the file to avoid overwriting
            if os.path.exists(target_file):
                base, ext = os.path.splitext(file_name)
                counter = 1
                new_file_name = f"{base}_dup{counter}{ext}"
                target_file = os.path.join(target_dir, new_file_name)
                # Ensure unique filename if multiple duplicates exist
                while os.path.exists(target_file):
                    counter += 1
                    new_file_name = f"{base}_dup{counter}{ext}"
                    target_file = os.path.join(target_dir, new_file_name)
            shutil.move(source_file, target_file)
            files_moved += 1
            print(f"Moved '{file_name}' to '{target_file}'")
    
    print(f"Total files moved: {files_moved}")
    
    # Attempt to remove the now-empty source directory
    try:
        os.rmdir(source_dir)
        print(f"Removed empty folder '{source_dir}'.")
    except Exception as e:
        print(f"Could not remove folder '{source_dir}': {e}")
