"""
Mô hình demo đơn giản để gán nhãn điều luật cho bản án
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import pickle
import os
from typing import List, Dict, Tuple, Optional
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_loader import DataLoader

class LawClassifier:
    """Mô hình phân loại điều luật cho bản án"""
    
    def __init__(self, model_type: str = 'naive_bayes'):
        self.model_type = model_type
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words=None,
            min_df=2,
            max_df=0.95
        )
        self.classifier = None
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
    def prepare_data(self, loader: DataLoader) -> Tuple[np.ndarray, np.ndarray]:
        """
        Chuẩn bị dữ liệu cho training
        
        Args:
            loader: DataLoader instance
            
        Returns:
            Tuple (X, y) - features và labels
        """
        print("📊 Chuẩn bị dữ liệu training...")
        
        # Lấy dữ liệu bản án với điều luật
        cases_with_laws = loader.get_case_with_laws()
        
        if len(cases_with_laws) == 0:
            print("❌ Không có dữ liệu để training")
            return np.array([]), np.array([])
        
        # Lọc dữ liệu có article hợp lệ (thay vì law_id)
        valid_data = cases_with_laws.dropna(subset=['article'])
        
        if len(valid_data) == 0:
            print("❌ Không có dữ liệu hợp lệ để training")
            return np.array([]), np.array([])
        
        # Chuẩn bị features (text của bản án)
        texts = valid_data['text'].fillna('')
        
        # Chuẩn bị labels (article thay vì law_id)
        labels = valid_data['article'].astype(str)
        
        print(f"✅ Đã chuẩn bị {len(texts)} samples")
        print(f"📊 Số lượng điều luật khác nhau: {labels.nunique()}")
        
        return texts, labels
    
    def train(self, loader: DataLoader, test_size: float = 0.2):
        """
        Huấn luyện mô hình
        
        Args:
            loader: DataLoader instance
            test_size: Tỷ lệ dữ liệu test
        """
        print(f"🚀 Bắt đầu training mô hình {self.model_type}...")
        
        # Chuẩn bị dữ liệu
        texts, labels = self.prepare_data(loader)
        
        if len(texts) == 0:
            print("❌ Không có dữ liệu để training")
            return
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(labels)
        
        # Split dữ liệu
        X_train, X_test, y_train, y_test = train_test_split(
            texts, y_encoded, test_size=test_size, random_state=42, stratify=y_encoded
        )
        
        print(f"📊 Training set: {len(X_train)} samples")
        print(f"📊 Test set: {len(X_test)} samples")
        
        # Vectorize text
        print("🔤 Đang vectorize text...")
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        X_test_vectorized = self.vectorizer.transform(X_test)
        
        # Chọn và huấn luyện classifier
        if self.model_type == 'naive_bayes':
            self.classifier = MultinomialNB()
        elif self.model_type == 'random_forest':
            self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Model type '{self.model_type}' không được hỗ trợ")
        
        print(f"🎯 Đang training {self.model_type}...")
        self.classifier.fit(X_train_vectorized, y_train)
        
        # Đánh giá mô hình
        self.evaluate_model(X_test_vectorized, y_test)
        
        self.is_trained = True
        print("✅ Training hoàn thành!")
    
    def evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray):
        """Đánh giá mô hình"""
        print("\n📈 ĐÁNH GIÁ MÔ HÌNH:")
        print("=" * 50)
        
        # Predict
        y_pred = self.classifier.predict(X_test)
        
        # Accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"🎯 Accuracy: {accuracy:.4f}")
        
        # Classification report - chỉ định labels để tránh lỗi
        unique_labels = np.unique(np.concatenate([y_test, y_pred]))
        target_names = [self.label_encoder.inverse_transform([label])[0] for label in unique_labels]
        
        print("\n📊 Classification Report:")
        print(classification_report(y_test, y_pred, labels=unique_labels, target_names=target_names))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n📋 Confusion Matrix Shape: {cm.shape}")
        
        # Top predictions
        print(f"\n🔝 Top 10 predictions:")
        unique, counts = np.unique(y_pred, return_counts=True)
        top_predictions = sorted(zip(unique, counts), key=lambda x: x[1], reverse=True)[:10]
        
        for i, (pred_class, count) in enumerate(top_predictions, 1):
            article = self.label_encoder.inverse_transform([pred_class])[0]
            print(f"  {i:2d}. Article {article}: {count} predictions")
    
    def predict(self, text: str) -> List[Dict]:
        """
        Dự đoán điều luật cho một bản án
        
        Args:
            text: Nội dung bản án
            
        Returns:
            List các dict chứa thông tin dự đoán
        """
        if not self.is_trained:
            print("❌ Mô hình chưa được training")
            return []
        
        # Vectorize text
        text_vectorized = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.classifier.predict(text_vectorized)[0]
        probabilities = self.classifier.predict_proba(text_vectorized)[0]
        
        # Lấy top 5 predictions
        top_indices = np.argsort(probabilities)[::-1][:5]
        
        results = []
        for i, idx in enumerate(top_indices):
            article = self.label_encoder.inverse_transform([idx])[0]
            confidence = probabilities[idx]
            
            results.append({
                'rank': i + 1,
                'article': str(article),
                'confidence': float(confidence),
                'probability': float(confidence)
            })
        
        return results
    
    def predict_batch(self, texts: List[str]) -> List[List[Dict]]:
        """
        Dự đoán cho nhiều bản án
        
        Args:
            texts: List các nội dung bản án
            
        Returns:
            List các predictions cho từng bản án
        """
        if not self.is_trained:
            print("❌ Mô hình chưa được training")
            return []
        
        # Vectorize texts
        texts_vectorized = self.vectorizer.transform(texts)
        
        # Predict
        predictions = self.classifier.predict(texts_vectorized)
        probabilities = self.classifier.predict_proba(texts_vectorized)
        
        results = []
        for i, (pred, probs) in enumerate(zip(predictions, probabilities)):
            # Lấy top 3 predictions cho mỗi bản án
            top_indices = np.argsort(probs)[::-1][:3]
            
            sample_results = []
            for j, idx in enumerate(top_indices):
                article = self.label_encoder.inverse_transform([idx])[0]
                confidence = probs[idx]
                
                sample_results.append({
                    'rank': j + 1,
                    'article': str(article),
                    'confidence': float(confidence)
                })
            
            results.append(sample_results)
        
        return results
    
    def save_model(self, filepath: str):
        """Lưu mô hình"""
        if not self.is_trained:
            print("❌ Mô hình chưa được training")
            return
        
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'label_encoder': self.label_encoder,
            'model_type': self.model_type
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✅ Đã lưu mô hình vào {filepath}")
    
    def load_model(self, filepath: str):
        """Load mô hình"""
        if not os.path.exists(filepath):
            print(f"❌ Không tìm thấy file {filepath}")
            return
        
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data['vectorizer']
        self.classifier = model_data['classifier']
        self.label_encoder = model_data['label_encoder']
        self.model_type = model_data['model_type']
        self.is_trained = True
        
        print(f"✅ Đã load mô hình từ {filepath}")


def demo_classifier():
    """Demo mô hình classifier"""
    print("🎯 DEMO: MÔ HÌNH PHÂN LOẠI ĐIỀU LUẬT")
    print("=" * 60)
    
    # Load dữ liệu
    loader = DataLoader()
    data = loader.load_all_data()
    
    if not data:
        print("❌ Không thể load dữ liệu")
        return
    
    # Tạo và training mô hình
    classifier = LawClassifier(model_type='naive_bayes')
    classifier.train(loader)
    
    # Test với một số bản án
    print("\n🧪 TEST PREDICTIONS:")
    print("=" * 40)
    
    # Lấy một số bản án để test
    test_cases = loader.case_data.head(3)
    
    for i, (_, case) in enumerate(test_cases.iterrows(), 1):
        print(f"\n📄 Test case {i}:")
        case_name = case['case_name'][:50] + "..." if len(case['case_name']) > 50 else case['case_name']
        print(f"  Tên bản án: {case_name}")
        
        # Predict
        predictions = classifier.predict(case['text'])
        
        print(f"  Dự đoán:")
        for pred in predictions[:3]:  # Top 3
            print(f"    {pred['rank']}. Article {pred['article']}: {pred['confidence']:.3f}")
    
    # Lưu mô hình
    classifier.save_model('models/law_classifier.pkl')
    
    print("\n✅ Demo hoàn thành!")


if __name__ == "__main__":
    # Tạo thư mục models nếu chưa có
    os.makedirs('models', exist_ok=True)
    demo_classifier() 