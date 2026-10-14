import os
import urllib.request
import time

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')]
urllib.request.install_opener(opener)

DATASET_IMAGES = {
    "elephant.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/African_Bush_Elephant.jpg/320px-African_Bush_Elephant.jpg",
    "bear.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/2010-kodiak-bear-1.jpg/320px-2010-kodiak-bear-1.jpg",
    "dog.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Labrador_Retriever_%281210559%29.jpg/320px-Labrador_Retriever_%281210559%29.jpg",
    "cat.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/320px-Cat_November_2010-1a.jpg"
}

AUDIO_FILES = {
    "Elephant": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Elephant_trumpet.ogg",
    "Bear": "https://upload.wikimedia.org/wikipedia/commons/4/41/Bear_Roar.ogg",
    "Dog": "https://upload.wikimedia.org/wikipedia/commons/1/15/Dog_barking.ogg",
    "Cat": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Cat_meow.ogg",
    "Cow": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Bovine_moo.ogg",
    "Sheep": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Sheep_bleat.ogg"
}

def download_files():
    print("Downloading Sample Dataset Images...")
    os.makedirs("dataset_sample", exist_ok=True)
    for name, url in DATASET_IMAGES.items():
        try:
            print(f"Downloading {name}...")
            urllib.request.urlretrieve(url, os.path.join("dataset_sample", name))
            time.sleep(2)
        except Exception as e:
            print(f"Failed to download {name}: {e}")

    print("\nDownloading Animal Audio Sounds...")
    os.makedirs("static/sounds", exist_ok=True)
    for name, url in AUDIO_FILES.items():
        try:
            print(f"Downloading {name} audio...")
            urllib.request.urlretrieve(url, os.path.join("static/sounds", f"{name}.ogg"))
            time.sleep(2)
        except Exception as e:
            print(f"Failed to download audio for {name}: {e}")

if __name__ == "__main__":
    download_files()
