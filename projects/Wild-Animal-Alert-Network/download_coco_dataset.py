from ultralytics.utils.downloads import download
import os
import shutil

print("Downloading COCO8 dataset (a small subset of the trained dataset)...")
download('https://github.com/ultralytics/yolov5/releases/download/v1.0/coco8.zip', dir='./dataset_sample')

print("Dataset downloaded and extracted to the 'dataset_sample/coco8' folder!")
print("These are examples of the training dataset images and labels used by YOLOv8.")
