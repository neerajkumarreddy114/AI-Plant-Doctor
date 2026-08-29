import torch
import torch.nn as nn

from torchvision.models import (
    mobilenet_v2,
    MobileNet_V2_Weights
)


# ==========================================
# 1. NUMBER OF CLASSES
# ==========================================

NUM_CLASSES = 38


# ==========================================
# 2. SELECT DEVICE
# ==========================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))


# ==========================================
# 3. LOAD PRETRAINED MOBILENETV2
# ==========================================

weights = MobileNet_V2_Weights.DEFAULT

model = mobilenet_v2(weights=weights)


# ==========================================
# 4. CHECK ORIGINAL CLASSIFIER
# ==========================================

print()
print("Original classifier:")
print(model.classifier)


# ==========================================
# 5. GET INPUT SIZE OF CLASSIFIER
# ==========================================

in_features = model.classifier[1].in_features

print()
print("Classifier input features:", in_features)


# ==========================================
# 6. REPLACE THE FINAL CLASSIFIER
# ==========================================

model.classifier[1] = nn.Linear(
    in_features,
    NUM_CLASSES
)


# ==========================================
# 7. MOVE MODEL TO GPU
# ==========================================

model = model.to(device)


# ==========================================
# 8. DISPLAY NEW CLASSIFIER
# ==========================================

print()
print("New classifier:")
print(model.classifier)


# ==========================================
# 9. TEST WITH A FAKE BATCH
# ==========================================

dummy_input = torch.randn(
    2, 3, 224, 224
).to(device)


with torch.no_grad():
    output = model(dummy_input)


print()
print("========== MODEL TEST ==========")

print("Input shape:", dummy_input.shape)
print("Output shape:", output.shape)
print("Expected output shape:", (2, NUM_CLASSES))