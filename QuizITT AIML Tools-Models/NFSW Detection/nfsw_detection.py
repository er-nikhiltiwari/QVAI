!pip install transformers torchvision torch pillow

!pip install transformers torch pdfplumber python-docx

import os
import pdfplumber
from docx import Document
from transformers import pipeline

classifier = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type. Use .pdf, .docx, or .txt")

def is_nsfw_content(text):
    results = classifier(text[:512])
    labels = results[0]
    toxic_score = sum([item["score"] for item in labels if item["label"] in ["toxicity", "obscene", "sexual_explicit", "threat"]])
    return "⚠️☠️🚨 Explicit/NSFW content detected ⚠️☠️🚨." if toxic_score > 0.5 else "✅👌 Content appears safe ✅🤝."

file_path = input("Enter the path of your file (.pdf/.docx/.txt): ").strip()

try:
    content = extract_text(file_path)
    result = is_nsfw_content(content)
    print(f"\n[RESULT]: The file content is likely => {result}")
except Exception as e:
    print("Error:", e)

"""NFSW detection for .img"""

from transformers import AutoProcessor, AutoModelForImageClassification
from PIL import Image
import torch

image_path = "images.png"
image = Image.open(image_path).convert("RGB")

model_name = "Falconsai/nsfw_image_detection"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = logits.argmax(-1).item()

labels = model.config.id2label
predicted_label = labels[predicted_class]

print(f"Prediction: {predicted_label}")
if predicted_label.lower() in ["porn", "nude", "nfsw", "explicit", "tits", "hentai", "vulgar", "sexy"]:
    print("⚠️☠️🚨 Explicit/NSFW content detected ⚠️☠️🚨.")
else:
    print("✅🤝 Content appears safe 🤝✅.")