import os
import shutil
from PIL import Image, UnidentifiedImageError
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.regularizers import l2


# ============================================================
# BASIC CONSTANTS
# ============================================================
CLASSES = ["normal", "pcos", "ovarian_cancer"]
NUM_CLASSES = len(CLASSES)
IMG_HEIGHT = 224
IMG_WIDTH = 224
TARGET_SIZE = (IMG_HEIGHT, IMG_WIDTH)

# ============================================================
# DIRECTORY STRUCTURE (AUTO DETECT)
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

SRC_DIR = os.path.join(BASE_DIR, "data", "images")
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned_images")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "resnet_gyne_model.h5")


# ============================================================
# CLEAN + PREPROCESS IMAGES
# ============================================================
def clean_and_preprocess_images(src_dir=SRC_DIR, out_dir=CLEAN_DIR):
    print("🧹 Cleaning & preprocessing images...")

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    found_images = 0

    for label in CLASSES:
        src_path = os.path.join(src_dir, label)
        dst_path = os.path.join(out_dir, label)

        if not os.path.exists(src_path):
            print(f"⚠️ Missing folder: {src_path} — skipping…")
            continue

        os.makedirs(dst_path, exist_ok=True)

        for file in os.listdir(src_path):
            file_path = os.path.join(src_path, file)

            if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            try:
                img = Image.open(file_path)
                img = img.convert("RGB").resize(TARGET_SIZE)
                img.save(os.path.join(dst_path, file))
                found_images += 1

            except UnidentifiedImageError:
                print(f"❌ Corrupted: {file_path}")

    print(f"✅ Cleaned {found_images} images.\n")


# ============================================================
# BUILD / LOAD MODEL
# ============================================================
def get_model(model_path=MODEL_PATH):

    if os.path.exists(model_path):
        print(f"🔄 Loading existing model from {model_path}")
        return load_model(model_path)

    print("🆕 Building new ResNet50 model…")

    base = ResNet50(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
    )

    # 🔥 Unfreeze last 30 layers for better learning (VERY IMPORTANT)
    for layer in base.layers[:-30]:
        layer.trainable = False
    for layer in base.layers[-30:]:
        layer.trainable = True

    x = GlobalAveragePooling2D()(base.output)
    x = Dropout(0.5)(x)
    x = Dense(256, activation="relu", kernel_regularizer=l2(0.001))(x)
    x = Dropout(0.3)(x)
    output = Dense(NUM_CLASSES, activation="softmax")(x)

    model = Model(inputs=base.input, outputs=output)

    model.compile(
        optimizer=Adam(1e-5),   # lowered LR for unfreezing layers
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ============================================================
# TRAIN MODEL
# ============================================================
def retrain_model():

    os.makedirs(MODEL_DIR, exist_ok=True)

    clean_and_preprocess_images()

    # STRONG AUGMENTATION TO FIX PCOS/OVARIAN CONFUSION
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        zoom_range=0.20,
        shear_range=0.15,
        brightness_range=[0.8, 1.2],
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=0.2
    )

    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_gen = train_datagen.flow_from_directory(
        CLEAN_DIR,
        classes=CLASSES,
        target_size=TARGET_SIZE,
        batch_size=16,
        class_mode="categorical",
        subset="training"
    )

    if train_gen.n == 0:
        print("❌ No images found. Check your dataset.")
        return

    val_gen = val_datagen.flow_from_directory(
        CLEAN_DIR,
        classes=CLASSES,
        target_size=TARGET_SIZE,
        batch_size=16,
        class_mode="categorical",
        subset="validation"
    )

    model = get_model()

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True)
    ]

    print("🚀 Training started...")

    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=60,
        callbacks=callbacks,
    )

    print(f"✅ Training finished! Model saved at {MODEL_PATH}")


if __name__ == "__main__":
    retrain_model()
