# HỆ THỐNG PHÂN TÍCH BẢN ÁN HÌNH SỰ

## 📋 Mô tả dự án

Hệ thống phân tích và gán nhãn điều luật cho bản án hình sự Việt Nam. Dự án sử dụng dữ liệu từ các file CSV đã được export từ database và bao gồm một mô hình demo đơn giản để phân loại điều luật.

## 📊 Dữ liệu

Dự án sử dụng 3 file CSV chính:

- **`data_export/case_data.csv`** - Dữ liệu bản án (10,001 records)
- **`data_export/law_data.csv`** - Dữ liệu điều luật (1,122 records)  
- **`data_export/case_law_data.csv`** - Mối quan hệ bản án - điều luật (13,470 records)

## 🏗️ Cấu trúc dự án

```
summer_project/
├── data_export/           # Dữ liệu CSV
│   ├── case_data.csv
│   ├── law_data.csv
│   ├── case_law_data.csv
│   └── README.md
├── src/                   # Source code
│   ├── data_loader.py     # Module load dữ liệu từ CSV
│   └── models/            # Các model ML
│       └── law_classifier.py  # Mô hình phân loại điều luật
├── models/                # Thư mục lưu mô hình đã train
├── notebooks/             # Jupyter notebooks
├── demo_model.py          # Script demo mô hình
└── requirements.txt       # Dependencies
```

## 🚀 Cách sử dụng

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Chạy demo mô hình

```bash
python demo_model.py
```

### 3. Sử dụng trong code

```python
from src.data_loader import DataLoader
from src.models.law_classifier import LawClassifier

# Load dữ liệu
loader = DataLoader()
data = loader.load_all_data()

# Tạo và training mô hình
classifier = LawClassifier(model_type='naive_bayes')
classifier.train(loader)

# Dự đoán cho một bản án
predictions = classifier.predict("Nội dung bản án...")
for pred in predictions:
    print(f"Law ID {pred['law_id']}: {pred['confidence']:.3f}")
```

## 📈 Tính năng chính

### DataLoader Class

- **`load_all_data()`** - Load tất cả dữ liệu từ CSV files
- **`get_data_info()`** - Lấy thông tin tổng quan về dữ liệu
- **`get_case_with_laws()`** - Lấy bản án kèm điều luật được áp dụng
- **`get_law_statistics()`** - Thống kê sử dụng điều luật
- **`get_case_statistics()`** - Thống kê bản án
- **`search_cases()`** - Tìm kiếm bản án theo từ khóa
- **`get_law_by_id()`** - Lấy thông tin điều luật theo ID
- **`get_case_by_id()`** - Lấy thông tin bản án theo ID

### LawClassifier Class

- **`train()`** - Huấn luyện mô hình phân loại
- **`predict()`** - Dự đoán điều luật cho một bản án
- **`predict_batch()`** - Dự đoán cho nhiều bản án
- **`evaluate_model()`** - Đánh giá hiệu suất mô hình
- **`save_model()`** - Lưu mô hình đã train
- **`load_model()`** - Load mô hình đã lưu

## 🤖 Mô hình ML

### Các loại mô hình hỗ trợ:
- **Naive Bayes** - Mô hình đơn giản, nhanh
- **Random Forest** - Mô hình ensemble, chính xác hơn

### Quy trình xử lý:
1. **Chuẩn bị dữ liệu**: Lọc và làm sạch dữ liệu bản án - điều luật
2. **Vectorize text**: Sử dụng TF-IDF để chuyển text thành vector
3. **Training**: Huấn luyện mô hình phân loại
4. **Đánh giá**: Tính accuracy, precision, recall, f1-score
5. **Dự đoán**: Trả về top-k điều luật có khả năng cao nhất

## 📊 Thống kê dữ liệu

- **Bản án**: 10,001 records
- **Điều luật**: 1,122 records
- **Mối quan hệ**: 13,470 records

## 🎯 Mục tiêu

1. **Phân tích dữ liệu**: Hiểu rõ cấu trúc và đặc điểm của bản án hình sự
2. **Gán nhãn tự động**: Xây dựng model để tự động gán điều luật cho bản án mới
3. **Đánh giá hiệu suất**: So sánh với baseline và cải thiện model

## 📝 Ghi chú

- Dữ liệu được export từ database với encoding UTF-8
- Mô hình sử dụng TF-IDF vectorization và Naive Bayes classifier
- Có thể mở rộng để sử dụng các mô hình deep learning như BERT
- Hệ thống được thiết kế để dễ dàng mở rộng và thêm tính năng mới

---

*Cập nhật: 2025-01-30* 