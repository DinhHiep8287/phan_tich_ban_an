"""
Demo script đơn giản để test mô hình phân loại điều luật
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader
from models.law_classifier import LawClassifier

def main():
    """Main function"""
    print("🎯 DEMO: MÔ HÌNH PHÂN LOẠI ĐIỀU LUẬT")
    print("=" * 60)
    
    # Load dữ liệu
    print("📊 Đang load dữ liệu...")
    loader = DataLoader()
    data = loader.load_all_data()
    
    if not data:
        print("❌ Không thể load dữ liệu")
        return
    
    print("✅ Đã load dữ liệu thành công!")
    
    # Tạo và training mô hình
    print("\n🚀 Bắt đầu training mô hình...")
    classifier = LawClassifier(model_type='naive_bayes')
    classifier.train(loader)
    
    # Test predictions
    print("\n🧪 TEST PREDICTIONS:")
    print("=" * 40)
    
    # Lấy một số bản án để test
    test_cases = loader.case_data.head(5)
    
    for i, (_, case) in enumerate(test_cases.iterrows(), 1):
        print(f"\n📄 Test case {i}:")
        case_name = case['case_name']
        if len(case_name) > 60:
            case_name = case_name[:60] + "..."
        print(f"  Tên bản án: {case_name}")
        
        # Predict
        predictions = classifier.predict(case['text'])
        
        print(f"  Dự đoán (top 3):")
        for pred in predictions[:3]:
            print(f"    {pred['rank']}. Article {pred['article']}: {pred['confidence']:.3f}")
    
    # Lưu mô hình
    print("\n💾 Lưu mô hình...")
    os.makedirs('models', exist_ok=True)
    classifier.save_model('models/law_classifier.pkl')
    
    print("\n✅ Demo hoàn thành!")

if __name__ == "__main__":
    main() 