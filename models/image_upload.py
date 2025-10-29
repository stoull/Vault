import requests
import os
from pathlib import Path


def batch_upload_images(folder_path, upload_url):
    """批量上传目录下的所有图片"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

    for file_path in Path(folder_path).iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': (file_path.name, f, 'image/jpeg')}
                    response = requests.post(upload_url, files=files)

                    print(f"上传 {file_path.name}: {response.status_code}")
                    if response.status_code == 200:
                        print(f"成功: {response.json()}")
                    else:
                        print(f"失败: {response.text}")

            except Exception as e:
                print(f"上传 {file_path.name} 时出错: {e}")


# 使用示例
if __name__ == "__main__":
    batch_upload_images('/path/to/your/images', 'http://localhost:5000/upload')

"""
#!/bin/bash

UPLOAD_URL="http://localhost:5000/upload"
IMAGE_DIR="/path/to/your/images"

for file in "$IMAGE_DIR"/*.{jpg,jpeg,png,gif}; do
    if [ -f "$file" ]; then
        echo "上传: $(basename "$file")"
        curl -X POST "$UPLOAD_URL" \
             -F "file=@$file" \
             -s -o response.json
        
        echo "状态: $(jq '.success' response.json 2>/dev/null || cat response.json)"
        echo "---"
    fi
done
"""