from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import os

BASE = os.path.dirname(os.path.dirname(__file__))
CLEAN_DIR = os.path.join(BASE, "data", "cleaned_images") if os.path.exists(os.path.join(BASE,"data","cleaned_images")) else os.path.join(BASE,"data","images")
CLASSES = ["normal","pcos","ovarian_cancer"]
TARGET_SIZE = (224,224)
MODEL_PATH = os.path.join(BASE,"models","resnet_gyne_model.h5")

model = load_model(MODEL_PATH)
val_gen = ImageDataGenerator(rescale=1./255, validation_split=0.2).flow_from_directory(
    CLEAN_DIR, classes=CLASSES, target_size=TARGET_SIZE, batch_size=16, class_mode='categorical', subset='validation', shuffle=False
)

y_pred_probs = model.predict(val_gen, steps=(val_gen.samples//val_gen.batch_size)+1)
y_pred = np.argmax(y_pred_probs, axis=1)
y_true = val_gen.classes[:len(y_pred)]

print("Confusion matrix:")
print(confusion_matrix(y_true, y_pred))
print("Classification report:")
print(classification_report(y_true, y_pred, target_names=CLASSES))
