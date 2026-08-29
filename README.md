# 🌿 AI Plant Doctor

AI Plant Doctor is an AI-powered plant disease detection application that identifies plant diseases from leaf images.

## 🚀 Features

- 🌱 Plant disease detection from leaf images
- 📷 Upload leaf images for prediction
- 🤖 MobileNetV2 deep learning model
- 🎯 38 disease classes
- 🌐 Multi-language interface
- 💊 Disease remedies and treatment information
- 🖥️ Simple and user-friendly interface
- ⚡ GPU support when available

## 🧠 Model

The application uses **MobileNetV2** for image classification.

The model predicts the disease based on the uploaded plant leaf image.

## 🛠️ Technologies Used

- Python
- PyTorch
- Torchvision
- Streamlit
- Pillow
- NumPy
- Matplotlib

## 📂 Project Structure

```text
AI-Plant-Doctor/
│
├── app.py
├── model.py
├── dataloader.py
├── train.py
├── test.py
├── evaluate.py
├── split_dataset.py
├── remedies.py
├── dataset_split.json
├── classification_report.txt
├── confusion_matrix.png
└── README.md
