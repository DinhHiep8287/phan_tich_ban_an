"""
Script cài đặt dự án gán nhãn điều luật
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Cài đặt các dependencies"""
    print("Đang cài đặt dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Cài đặt dependencies thành công!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi cài đặt dependencies: {e}")
        return False
    return True

def create_env_file():
    """Tạo file .env từ template"""
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if not env_file.exists() and env_example.exists():
        print("Tạo file .env từ template...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Đã tạo file .env")
        print("⚠️  Vui lòng cập nhật thông tin database trong file .env")
    else:
        print("✅ File .env đã tồn tại")

def create_directories():
    """Tạo các thư mục cần thiết"""
    directories = [
        "data",
        "src/extraction",
        "src/models", 
        "src/evaluation",
        "notebooks"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Đã tạo cấu trúc thư mục")

def main():
    """Hàm chính cài đặt"""
    print("🚀 Bắt đầu cài đặt dự án gán nhãn điều luật...")
    
    # Tạo thư mục
    create_directories()
    
    # Cài đặt dependencies
    if not install_requirements():
        print("❌ Cài đặt thất bại!")
        return
    
    # Tạo file .env
    create_env_file()
    
    print("\n" + "="*50)
    print("✅ Cài đặt hoàn tất!")
    print("="*50)
    print("\nCác bước tiếp theo:")
    print("1. Cập nhật thông tin database trong file .env")
    print("2. Import dataset vào MySQL")
    print("3. Chạy: python src/extraction/law_extractor.py")
    print("4. Chạy: python src/models/baseline_models.py")
    print("5. Chạy: python src/evaluation/evaluate.py")

if __name__ == "__main__":
    main() 