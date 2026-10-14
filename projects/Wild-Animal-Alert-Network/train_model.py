from ultralytics import YOLO

# This script demonstrates how you would train the YOLOv8 model on your own custom dataset.
# Note: Training requires a powerful GPU and can take several hours depending on the dataset size.

def train_custom_model():
    print("Loading the base YOLOv8 model...")
    # Load a pretrained model (recommended for training)
    model = YOLO('yolov8s.pt') 

    print("Starting training process...")
    # Train the model using the 'coco8.yaml' dataset configuration 
    # (You would replace 'coco8.yaml' with your own custom dataset YAML file)
    results = model.train(
        data='coco8.yaml', # Path to dataset configuration file
        epochs=10,         # Number of training epochs (increase to 100+ for real training)
        imgsz=640,         # Image size for training
        batch=8,           # Batch size
        name='wild_animal_custom_model' # Name of the folder to save the trained weights
    )
    
    print("\nTraining completed!")
    print("Your newly trained model weights are saved in the 'runs/detect/wild_animal_custom_model/weights/best.pt' folder.")

if __name__ == '__main__':
    # Uncomment the line below to actually run the training process!
    # train_custom_model()
    print("Training script is ready. Open train_model.py and uncomment 'train_custom_model()' to begin training.")
