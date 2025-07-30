# DỮ LIỆU EXPORT TỪ DATABASE

## 📊 Thống kê tổng quan
- **Bảng 'case'**: 10,001 records
- **Bảng 'law'**: 1,122 records  
- **Bảng 'case_law'**: 13,470 records

## 📁 Files được tạo
1. `case_data.csv` - Dữ liệu bản án
2. `law_data.csv` - Dữ liệu điều luật
3. `case_law_data.csv` - Mối quan hệ bản án - điều luật

## 📋 Cấu trúc dữ liệu

### Bảng 'case'
- Số cột: 13
- Cột: id, case_number, case_name, document_type, case_level, law_type, court_name, content, text, created, uploaded, url, file

### Bảng 'law'  
- Số cột: 5
- Cột: id, article, title, content, type

### Bảng 'case_law'
- Số cột: 7
- Cột: id, case_id, law_id, point, clause, article, type

## 🎯 Sử dụng
- Dữ liệu được export với encoding UTF-8
- Có thể mở bằng Excel hoặc pandas
- Sẵn sàng cho phân tích và xử lý

---
*Generated on: 2025-07-30 11:17:51*
