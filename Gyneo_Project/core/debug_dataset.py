import os
SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "images")
print("Looking at:", SRC_DIR)
for cls in ("normal","pcos","ovarian_cancer"):
    path = os.path.join(SRC_DIR, cls)
    if not os.path.exists(path):
        print(f" MISSING: {path}")
    else:
        count = 0
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith((".jpg",".jpeg",".png")):
                    count += 1
        print(f" {cls}: {count} images (path={path})")
