import urllib.request
import os

# Create directory if not exists
os.makedirs(r'D:\AI_Files', exist_ok=True)

# Download image
url = "https://fastly.picsum.photos/id/296/800/1000.jpg?hmac=OxErMMf0B3kTcxiOPsNWNkYHdvWml22oDqoP3BMU2xU"
output_path = r'D:\AI_Files\ai_image.jpg'

try:
    urllib.request.urlretrieve(url, output_path)
    print(f"Image downloaded successfully to {output_path}")
except Exception as e:
    print(f"Error: {e}")
