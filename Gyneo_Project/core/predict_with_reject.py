import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import os, sys

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "resnet_gyne_model.h5")
TARGET_SIZE = (224,224)
CLASSES = ["normal","pcos","ovarian_cancer"]
THRESHOLD = 0.60

model = load_model(MODEL_PATH)

def preprocess_image(path):
    img = Image.open(path).convert("RGB").resize(TARGET_SIZE)
    arr = np.array(img)/255.0
    return arr[np.newaxis, ...]

def predict_file(path):
    x = preprocess_image(path)
    probs = model.predict(x)[0]
    idx = int(np.argmax(probs))
    maxp = float(probs[idx])
    if maxp < THRESHOLD:
        return {"label":"unknown","confidence":maxp, "probs": dict(zip(CLASSES, [float(p) for p in probs]))}
    else:
        return {"label": CLASSES[idx], "confidence": maxp, "probs": dict(zip(CLASSES, [float(p) for p in probs]))}

if __name__ == "__main__":
    p = sys.argv[1]
    print(predict_file(p))
