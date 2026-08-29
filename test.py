import torch
import torch.nn as nn

from torchvision.models import mobilenet_v2

from dataloader import test_loader


# ==================================================
# 1. SETTINGS
# ==================================================

NUM_CLASSES = 38

MODEL_PATH = "best_model.pth"

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ==================================================
# 2. DISPLAY DEVICE
# ==================================================

print("========================================")
print("       PLANT DISEASE TESTING")
print("========================================")

print("Device:", device)

if torch.cuda.is_available():
    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ==================================================
# 3. CREATE MOBILE NET V2
# ==================================================

model = mobilenet_v2(
    weights=None
)


# ==================================================
# 4. REPLACE CLASSIFIER
# ==================================================

in_features = model.classifier[1].in_features

model.classifier[1] = nn.Linear(
    in_features,
    NUM_CLASSES
)


# ==================================================
# 5. LOAD TRAINED MODEL
# ==================================================

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)


# ==================================================
# 6. MOVE MODEL TO GPU
# ==================================================

model = model.to(device)


# ==================================================
# 7. EVALUATION MODE
# ==================================================

model.eval()


# ==================================================
# 8. LOSS FUNCTION
# ==================================================

criterion = nn.CrossEntropyLoss()


# ==================================================
# 9. TEST MODEL
# ==================================================

total_loss = 0.0
correct = 0
total = 0


print()
print("Testing model...")
print()


with torch.no_grad():

    for images, labels in test_loader:

        # Move images and labels to GPU
        images = images.to(device)
        labels = labels.to(device)

        # Model prediction
        outputs = model(images)

        # Calculate loss
        loss = criterion(
            outputs,
            labels
        )

        total_loss += loss.item()

        # Get predicted class
        predictions = outputs.argmax(
            dim=1
        )

        # Count correct predictions
        correct += (
            predictions == labels
        ).sum().item()

        # Count total images
        total += labels.size(0)


# ==================================================
# 10. CALCULATE RESULTS
# ==================================================

test_loss = (
    total_loss / len(test_loader)
)

test_accuracy = (
    100 * correct / total
)


# ==================================================
# 11. DISPLAY RESULTS
# ==================================================

print("========================================")
print("          FINAL TEST RESULTS")
print("========================================")

print(
    f"Test images: {total}"
)

print(
    f"Correct predictions: {correct}"
)

print(
    f"Incorrect predictions: {total - correct}"
)

print(
    f"Test Loss: {test_loss:.4f}"
)

print(
    f"Test Accuracy: {test_accuracy:.2f}%"
)

print()
print("========================================")
print("          TESTING COMPLETE")
print("========================================")