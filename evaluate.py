import torch
import torch.nn as nn

from torchvision.models import mobilenet_v2

from sklearn.metrics import (
    confusion_matrix,
    classification_report
)

import matplotlib.pyplot as plt

from dataloader import test_loader, class_names


# ==================================================
# 1. SETTINGS
# ==================================================

NUM_CLASSES = 38
MODEL_PATH = "best_model.pth"

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ==================================================
# 2. DISPLAY INFORMATION
# ==================================================

print("========================================")
print("      DETAILED MODEL EVALUATION")
print("========================================")

print("Device:", device)

if torch.cuda.is_available():
    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ==================================================
# 3. CREATE MOBILENETV2
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
# 5. LOAD BEST MODEL
# ==================================================

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(device)

model.eval()


# ==================================================
# 6. COLLECT PREDICTIONS
# ==================================================

all_labels = []
all_predictions = []


print()
print("Running predictions on test dataset...")
print()


with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)

        outputs = model(images)

        predictions = outputs.argmax(
            dim=1
        )

        all_labels.extend(
            labels.cpu().numpy()
        )

        all_predictions.extend(
            predictions.cpu().numpy()
        )


# ==================================================
# 7. CONFUSION MATRIX
# ==================================================

cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=list(range(NUM_CLASSES))
)


# ==================================================
# 8. CLASSIFICATION REPORT
# ==================================================

report = classification_report(
    all_labels,
    all_predictions,
    labels=list(range(NUM_CLASSES)),
    target_names=class_names,
    digits=4,
    zero_division=0
)


print("========================================")
print("       CLASSIFICATION REPORT")
print("========================================")

print(report)


# ==================================================
# 9. OVERALL ACCURACY
# ==================================================

correct = sum(
    true == pred
    for true, pred
    in zip(all_labels, all_predictions)
)

total = len(all_labels)

accuracy = (
    100 * correct / total
)


print("========================================")
print("         EVALUATION SUMMARY")
print("========================================")

print("Total test images:", total)
print("Correct:", correct)
print("Incorrect:", total - correct)
print(f"Accuracy: {accuracy:.2f}%")


# ==================================================
# 10. SAVE CLASSIFICATION REPORT
# ==================================================

with open(
    "classification_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(report)

    file.write("\n\n")

    file.write(
        f"Overall Accuracy: {accuracy:.2f}%\n"
    )


# ==================================================
# 11. CREATE CONFUSION MATRIX PLOT
# ==================================================

plt.figure(
    figsize=(20, 18)
)

plt.imshow(cm)

plt.title(
    "Plant Disease Confusion Matrix"
)

plt.xlabel(
    "Predicted Class"
)

plt.ylabel(
    "Actual Class"
)

plt.xticks(
    range(NUM_CLASSES),
    class_names,
    rotation=90,
    fontsize=7
)

plt.yticks(
    range(NUM_CLASSES),
    class_names,
    fontsize=7
)

plt.colorbar()

plt.tight_layout()

plt.savefig(
    "confusion_matrix.png",
    dpi=300
)

plt.close()


print()
print("Confusion matrix saved:")
print("confusion_matrix.png")

print()
print("Classification report saved:")
print("classification_report.txt")

print()
print("========================================")
print("       EVALUATION COMPLETE")
print("========================================")