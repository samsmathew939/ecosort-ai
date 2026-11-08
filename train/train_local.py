"""Train the EcoSort YOLOv8 classifier on TrashNet, locally on CPU.

Produces real weights at ../models/ecosort.pt and prints real validation
accuracy. Run from the repo root inside the venv:

    .venv/Scripts/python.exe train/train_local.py

This is the local-CPU equivalent of EcoSort_TrainTrashNet.ipynb (Colab/GPU).
Same dataset, same model, same classes — just no GPU required.
"""
import random
import shutil
import urllib.request
import zipfile
from pathlib import Path

from ultralytics import YOLO

EPOCHS = 12          # enough for a solid, honest demo model on CPU
IMGSZ = 224
BATCH = 32
CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
ZIP_URL = "https://github.com/garythung/trashnet/raw/master/data/dataset-resized.zip"

here = Path(__file__).resolve().parent
repo = here.parent
data_root = here / "trashnet"

# 1. Download TrashNet (original resized zip) and build train/val folders
if not data_root.exists():
    zip_path = here / "dataset-resized.zip"
    if not zip_path.exists():
        print("Downloading TrashNet...")
        urllib.request.urlretrieve(ZIP_URL, zip_path)
    extract_dir = here / "_extract"
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(extract_dir)
    src = extract_dir / "dataset-resized"

    random.seed(42)
    for cls in CLASSES:
        imgs = sorted(p for p in (src / cls).glob("*.jpg"))
        random.shuffle(imgs)
        split = int(0.8 * len(imgs))
        for phase, group in {"train": imgs[:split], "val": imgs[split:]}.items():
            d = data_root / phase / cls
            d.mkdir(parents=True, exist_ok=True)
            for p in group:
                shutil.copy(p, d / p.name)
    print("Built dataset folders.")

# 2. Train
model = YOLO("yolov8n-cls.pt")
results = model.train(data=str(data_root), epochs=EPOCHS, imgsz=IMGSZ,
                      batch=BATCH, seed=42, device="cpu")

# 3. Real validation accuracy (cite these numbers, don't round up)
metrics = model.val()
print(f"\nTop-1 accuracy: {metrics.top1:.3f}")
print(f"Top-5 accuracy: {metrics.top5:.3f}")

# 4. Save weights into the app
best = Path(results.save_dir) / "weights" / "best.pt"
dest = repo / "models" / "ecosort.pt"
dest.parent.mkdir(exist_ok=True)
shutil.copy(best, dest)
print(f"\nSaved weights -> {dest} ({dest.stat().st_size/1e6:.1f} MB)")
