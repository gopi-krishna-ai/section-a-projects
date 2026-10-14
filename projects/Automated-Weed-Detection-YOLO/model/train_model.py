"""
Automated Weed Detection System Using YOLO - model training.

Fine-tunes a YOLOv8-nano model (pretrained on COCO) on the real
crop/weed dataset via transfer learning, exactly as described in the
project abstract ("Transfer learning further accelerates the training
process by utilizing pre-trained YOLO weights"). Requires an internet
connection the first time it runs, to download the base yolov8n.pt
COCO weights - the resulting app does not call any external API at
inference time.

Run:
    python train_model.py [--epochs 30] [--imgsz 416] [--batch 8]
"""

import argparse
import os
import shutil

from ultralytics import YOLO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_YAML = os.path.join(BASE_DIR, "data", "yolo_dataset", "data.yaml")
RUNS_DIR = os.path.join(BASE_DIR, "model", "runs")
FINAL_MODEL_PATH = os.path.join(BASE_DIR, "model", "weed_yolo_best.pt")
RUN_NAME = "weed_train"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    args = parser.parse_args()

    if not os.path.exists(DATA_YAML):
        raise FileNotFoundError("Run 'python data/prepare_dataset.py' first.")

    model = YOLO("yolov8n.pt")
    model.train(
        data=DATA_YAML,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=RUNS_DIR,
        name=RUN_NAME,
        exist_ok=True,
        patience=15,
        cos_lr=True,
        close_mosaic=10,
        degrees=3.0,
        translate=0.08,
        scale=0.5,
        fliplr=0.5,
        mosaic=0.8,
        mixup=0.1,
        verbose=True,
    )

    best_path = os.path.join(RUNS_DIR, RUN_NAME, "weights", "best.pt")
    shutil.copy2(best_path, FINAL_MODEL_PATH)
    print(f"Best weights copied -> {FINAL_MODEL_PATH}")

    metrics = model.val(data=DATA_YAML)
    print("\nFinal validation metrics:")
    print(f"  mAP50:    {metrics.box.map50:.3f}")
    print(f"  mAP50-95: {metrics.box.map:.3f}")
    print(f"  Precision:{metrics.box.mp:.3f}")
    print(f"  Recall:   {metrics.box.mr:.3f}")


if __name__ == "__main__":
    main()
