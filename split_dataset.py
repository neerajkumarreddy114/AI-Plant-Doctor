import json
import os

from torchvision import datasets
from sklearn.model_selection import train_test_split


# 1. Location of our dataset
dataset_path = r"C:\pd detection\dataset\color"

# 2. Load the dataset
dataset = datasets.ImageFolder(dataset_path)

# 3. Get all image paths and their class labels
image_paths = [item[0] for item in dataset.samples]
labels = [item[1] for item in dataset.samples]

print("Total images:", len(image_paths))
print("Total classes:", len(dataset.classes))

# 4. First split:
#    80% training
#    20% temporary (validation + test)

train_paths, temp_paths, train_labels, temp_labels = train_test_split(
    image_paths,
    labels,
    test_size=0.20,
    stratify=labels,
    random_state=42
)

# 5. Split the temporary 20% into:
#    10% validation
#    10% test

val_paths, test_paths, val_labels, test_labels = train_test_split(
    temp_paths,
    temp_labels,
    test_size=0.50,
    stratify=temp_labels,
    random_state=42
)

# 6. Put everything into one dictionary
split_data = {
    "train": train_paths,
    "validation": val_paths,
    "test": test_paths,
    "classes": dataset.classes
}

# 7. Save the split information
output_file = r"C:\pd detection\dataset_split.json"

with open(output_file, "w") as f:
    json.dump(split_data, f, indent=2)

# 8. Display results
print("\n========== DATASET SPLIT ==========")
print("Training images:   ", len(train_paths))
print("Validation images: ", len(val_paths))
print("Test images:       ", len(test_paths))
print("Total:             ", len(train_paths) + len(val_paths) + len(test_paths))

print("\nClasses:")
for number, class_name in enumerate(dataset.classes):
    print(number, "=", class_name)

print("\nSplit information saved to:")
print(output_file)