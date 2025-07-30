"""
Script test mô hình với input tùy chỉnh
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models.law_classifier import LawClassifier

def test_custom_input():
    """Test mô hình với input tùy chỉnh"""
    print("🧪 TEST MÔ HÌNH VỚI INPUT TÙY CHỈNH")
    print("=" * 60)
    
    # Load mô hình đã train
    classifier = LawClassifier()
    
    if os.path.exists('models/law_classifier.pkl'):
        classifier.load_model('models/law_classifier.pkl')
        print("✅ Đã load mô hình thành công!")
    else:
        print("❌ Không tìm thấy mô hình đã train. Hãy chạy demo_model.py trước.")
        return
    
    # Test cases
    test_cases = [
        {
            "name": "Tội giết người",
            "text": "Bị cáo Nguyễn Văn A đã dùng dao đâm chết nạn nhân trong lúc cãi vã. Hành vi này vi phạm quy định về bảo vệ tính mạng con người."
        },
        {
            "name": "Tội trộm cắp tài sản",
            "text": "Bị cáo đã lén lút vào nhà người khác và lấy trộm tài sản có giá trị. Hành vi này xâm phạm quyền sở hữu tài sản của công dân."
        },
        {
            "name": "Tội buôn bán ma túy",
            "text": "Bị cáo đã vận chuyển và buôn bán heroin trái phép. Hành vi này vi phạm quy định về phòng chống ma túy."
        },
        {
            "name": "Tội cho vay lãi nặng",
            "text": "Bị cáo đã cho vay tiền với lãi suất cao hơn quy định của pháp luật. Hành vi này vi phạm quy định về cho vay lãi nặng."
        },
        {
            "name": "Tội vi phạm quy định về giao thông",
            "text": "Bị cáo đã điều khiển xe máy vượt đèn đỏ và gây tai nạn giao thông. Hành vi này vi phạm quy định về an toàn giao thông."
        }
    ]
    
    print("\n📋 KẾT QUẢ DỰ ĐOÁN:")
    print("=" * 40)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📄 Test case {i}: {case['name']}")
        print(f"  Nội dung: {case['text'][:100]}...")
        
        # Predict
        predictions = classifier.predict(case['text'])
        
        print(f"  Dự đoán (top 5):")
        for pred in predictions[:5]:
            print(f"    {pred['rank']}. Article {pred['article']}: {pred['confidence']:.3f}")
    
    print("\n✅ Test hoàn thành!")

def interactive_test():
    """Test tương tác"""
    print("\n🎯 TEST TƯƠNG TÁC")
    print("=" * 40)
    
    # Load mô hình
    classifier = LawClassifier()
    
    if os.path.exists('models/law_classifier.pkl'):
        classifier.load_model('models/law_classifier.pkl')
        print("✅ Đã load mô hình thành công!")
    else:
        print("❌ Không tìm thấy mô hình đã train.")
        return
    
    print("\n💡 Nhập nội dung bản án để dự đoán điều luật:")
    print("   (Nhập 'quit' để thoát)")
    
    while True:
        print("\n" + "-" * 50)
        text = input("📝 Nội dung bản án: ")
        
        if text.lower() == 'quit':
            break
        
        if len(text.strip()) == 0:
            print("❌ Vui lòng nhập nội dung!")
            continue
        
        # Predict
        predictions = classifier.predict(text)
        
        print(f"\n🔍 KẾT QUẢ DỰ ĐOÁN:")
        for pred in predictions[:5]:
            print(f"  {pred['rank']}. Article {pred['article']}: {pred['confidence']:.3f}")
    
    print("\n👋 Tạm biệt!")

def main():
    """Main function"""
    print("🎯 TEST MÔ HÌNH PHÂN LOẠI ĐIỀU LUẬT")
    print("=" * 60)
    
    # Test với các case có sẵn
    test_custom_input()
    
    # Test tương tác
    interactive_test()

if __name__ == "__main__":
    main() 