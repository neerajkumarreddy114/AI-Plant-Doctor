import torch
import torch.nn as nn
import torch.optim as optim

from torchvision.models import (
    mobilenet_v2,
    MobileNet_V2_Weights
)

from dataloader import (
    train_loader,
    val_loader,
    class_names
)


# ==================================================
# 1. SETTINGS
# ==================================================

NUM_CLASSES = 38
EPOCHS = 5
LEARNING_RATE = 0.001

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("========================================")
print("       PLANT DISEASE TRAINING")
print("========================================")

print("Device:", device)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))


# ==================================================
# 2. LOAD PRETRAINED MOBILENETV2
# ==================================================

weights = MobileNet_V2_Weights.DEFAULT

model = mobilenet_v2(weights=weights)


# ==================================================
# 3. FREEZE FEATURE EXTRACTOR
# ==================================================

for parameter in model.features.parameters():
    parameter.requires_grad = False


# ==================================================
# 4. REPLACE CLASSIFIER
# ==================================================

in_features = model.classifier[1].in_features

model.classifier[1] = nn.Linear(
    in_features,
    NUM_CLASSES
)


# ==================================================
# 5. MOVE MODEL TO GPU
# ==================================================

model = model.to(device)


# ==================================================
# 6. LOSS FUNCTION
# ==================================================

criterion = nn.CrossEntropyLoss()


# ==================================================
# 7. OPTIMIZER
# ==================================================

optimizer = optim.Adam(
    model.classifier.parameters(),
    lr=LEARNING_RATE
)


# ==================================================
# 8. TRAINING FUNCTION
# ==================================================

def train_one_epoch():

    model.train()

    total_loss = 0
    correct = 0
    total = 0

    for images, labels in train_loader:

        # Move data to GPU
        images = images.to(device)
        labels = labels.to(device)

        # Clear old gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(images)

        # Calculate loss
        loss = criterion(outputs, labels)

        # Backpropagation
        loss.backward()

        # Update model weights
        optimizer.step()

        # Statistics
        total_loss += loss.item()

        predictions = outputs.argmax(dim=1)

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)


    average_loss = total_loss / len(train_loader)

    accuracy = 100 * correct / total

    return average_loss, accuracy


# ==================================================
# 9. VALIDATION FUNCTION
# ==================================================

def validate():

    model.eval()

    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            # Move data to GPU
            images = images.to(device)
            labels = labels.to(device)

            # Prediction
            outputs = model(images)

            # Loss
            loss = criterion(outputs, labels)

            total_loss += loss.item()

            # Prediction class
            predictions = outputs.argmax(dim=1)

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)


    average_loss = total_loss / len(val_loader)

    accuracy = 100 * correct / total

    return average_loss, accuracy


# ==================================================
# 10. TRAINING
# ==================================================

best_val_accuracy = 0.0


for epoch in range(EPOCHS):

    print()
    print(
        f"========== EPOCH {epoch + 1}/{EPOCHS} =========="
    )

    # Training
    train_loss, train_accuracy = train_one_epoch()

    print(
        f"Train Loss: {train_loss:.4f}"
    )

    print(
        f"Train Accuracy: {train_accuracy:.2f}%"
    )


    # Validation
    val_loss, val_accuracy = validate()

    print(
        f"Validation Loss: {val_loss:.4f}"
    )

    print(
        f"Validation Accuracy: {val_accuracy:.2f}%"
    )


    # ==================================================
    # SAVE BEST MODEL
    # ==================================================

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "class_names": class_names,
                "num_classes": NUM_CLASSES,
                "validation_accuracy": val_accuracy
            },
            "best_model.pth"
        )

        print("✅ New best model saved!")


# ==================================================
# 11. FINISHED
# ==================================================

print()
print("========================================")
print("          TRAINING COMPLETE")
print("========================================")

print(
    f"Best validation accuracy: "
    f"{best_val_accuracy:.2f}%"
)

print("Best model: best_model.pth")