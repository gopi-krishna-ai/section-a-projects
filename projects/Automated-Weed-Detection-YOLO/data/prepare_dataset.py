"""
Automated Weed Detection System Using YOLO - dataset preparation.

Source: Kaggle "Crop and Weed Detection Data with Bounding Boxes"
(ravirajsinh45) - 1,300 real 512x512 sesame-crop field images, each
with a YOLO-format label file (class x_center y_center width height,
normalized). Two classes: 0=crop, 1=weed.

This script splits the raw data/kaggle_reference/agri_data/data files
into the images/labels + train/val folder layout the `ultralytics`
YOLO trainer expects, and writes data.yaml describing it.

Run:
    python prepare_dataset.py
"""

import os
import random
import shutil

random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "kaggle_reference", "agri_data", "data")
OUT_DIR = os.path.join(BASE_DIR, "yolo_dataset")
VAL_FRACTION = 0.15


def main():
    stems = sorted(
        fname[:-5] for fname in os.listdir(RAW_DIR) if fname.endswith(".jpeg")
    )
    stems = [s for s in stems if os.path.exists(os.path.join(RAW_DIR, s + ".txt"))]
    random.shuffle(stems)

    n_val = max(1, int(len(stems) * VAL_FRACTION))
    val_stems = set(stems[:n_val])

    for split in ("train", "val"):
        os.makedirs(os.path.join(OUT_DIR, "images", split), exist_ok=True)
        os.makedirs(os.path.join(OUT_DIR, "labels", split), exist_ok=True)

    for stem in stems:
        split = "val" if stem in val_stems else "train"
        shutil.copy2(
            os.path.join(RAW_DIR, stem + ".jpeg"),
            os.path.join(OUT_DIR, "images", split, stem + ".jpeg"),
        )
        shutil.copy2(
            os.path.join(RAW_DIR, stem + ".txt"),
            os.path.join(OUT_DIR, "labels", split, stem + ".txt"),
        )

    data_yaml = f"""\
path: {OUT_DIR}
train: images/train
val: images/val
names:
  0: crop
  1: weed
"""
    with open(os.path.join(OUT_DIR, "data.yaml"), "w") as f:
        f.write(data_yaml)

    print(f"Total images: {len(stems)}  train: {len(stems) - n_val}  val: {n_val}")
    print(f"Dataset written -> {OUT_DIR}")
    print(f"data.yaml -> {os.path.join(OUT_DIR, 'data.yaml')}")


if __name__ == "__main__":
    main()
