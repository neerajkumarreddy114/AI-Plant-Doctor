import json
import torch

from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms


# ==========================================
# 1. LOAD OUR DATASET SPLIT
# ==========================================

with open("dataset_split.json", "r") as f:
    split_data = json.load(f)


train_paths = split_data["train"]
val_paths = split_data["validation"]
test_paths = split_data["test"]

class_names = split_data["classes"]


print("Training images:", len(train_paths))
print("Validation images:", len(val_paths))
print("Test images:", len(test_paths))
print("Number of classes:", len(class_names))


# ==========================================
# 2. IMAGE TRANSFORMATIONS
# ==========================================

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ==========================================
# 3. CREATE OUR CUSTOM DATASET
# ==========================================

class PlantDiseaseDataset(Dataset):

    def __init__(self, image_paths, transform=None):

        self.image_paths = image_paths
        self.transform = transform

    def __len__(self):

        return len(self.image_paths)

    def __getitem__(self, index):

        image_path = self.image_paths[index]

        image = Image.open(image_path).convert("RGB")

        # Get class name from folder name
        class_name = image_path.split("\\")[-2]

        # Find class number
        label = class_names.index(class_name)

        if self.transform:
            image = self.transform(image)

        return image, label


# ==========================================
# 4. CREATE DATASETS
# ==========================================

train_dataset = PlantDiseaseDataset(
    train_paths,
    train_transform
)

val_dataset = PlantDiseaseDataset(
    val_paths,
    test_transform
)

test_dataset = PlantDiseaseDataset(
    test_paths,
    test_transform
)


# ==========================================
# 5. CREATE DATALOADERS
# ==========================================

batch_size = 32

train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=0
)

test_loader = DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=0
)


# ==========================================
# 6. CHECK ONE BATCH
# ==========================================

images, labels = next(iter(train_loader))

print()
print("========== DATALOADER TEST ==========")

print("Image batch shape:", images.shape)
print("Label batch shape:", labels.shape)

print("First image label:", labels[0].item())
print("First image class:", class_names[labels[0].item()])


# ==========================================
# 7. CHECK GPU
# ==========================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print()
print("Device:", device)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))