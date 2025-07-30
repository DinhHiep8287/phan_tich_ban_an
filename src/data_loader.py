"""
Module load và xử lý dữ liệu từ các file CSV có sẵn
"""

import pandas as pd
import os
from typing import Dict, List, Tuple, Optional
import numpy as np

class DataLoader:
    """Lớp load và xử lý dữ liệu từ CSV files"""
    
    def __init__(self, data_dir: str = "data_export"):
        self.data_dir = data_dir
        self.case_data = None
        self.law_data = None
        self.case_law_data = None
        
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load tất cả dữ liệu từ các file CSV
        
        Returns:
            Dict chứa 3 DataFrame: case, law, case_law
        """
        print("📊 Đang load dữ liệu từ CSV files...")
        
        try:
            # Load case data
            case_file = os.path.join(self.data_dir, "case_data.csv")
            if os.path.exists(case_file):
                self.case_data = pd.read_csv(case_file, encoding='utf-8-sig')
                print(f"✅ Đã load {len(self.case_data):,} records từ case_data.csv")
            else:
                print(f"❌ Không tìm thấy file {case_file}")
                self.case_data = pd.DataFrame()
            
            # Load law data
            law_file = os.path.join(self.data_dir, "law_data.csv")
            if os.path.exists(law_file):
                self.law_data = pd.read_csv(law_file, encoding='utf-8-sig')
                print(f"✅ Đã load {len(self.law_data):,} records từ law_data.csv")
            else:
                print(f"❌ Không tìm thấy file {law_file}")
                self.law_data = pd.DataFrame()
            
            # Load case_law data
            case_law_file = os.path.join(self.data_dir, "case_law_data.csv")
            if os.path.exists(case_law_file):
                self.case_law_data = pd.read_csv(case_law_file, encoding='utf-8-sig')
                print(f"✅ Đã load {len(self.case_law_data):,} records từ case_law_data.csv")
            else:
                print(f"❌ Không tìm thấy file {case_law_file}")
                self.case_law_data = pd.DataFrame()
            
            return {
                'case': self.case_data,
                'law': self.law_data,
                'case_law': self.case_law_data
            }
            
        except Exception as e:
            print(f"❌ Lỗi load dữ liệu: {e}")
            return {}
    
    def get_data_info(self) -> Dict:
        """Lấy thông tin tổng quan về dữ liệu"""
        info = {}
        
        if self.case_data is not None:
            info['case'] = {
                'records': len(self.case_data),
                'columns': list(self.case_data.columns),
                'sample': self.case_data.head(1).to_dict('records')[0] if len(self.case_data) > 0 else {}
            }
        
        if self.law_data is not None:
            info['law'] = {
                'records': len(self.law_data),
                'columns': list(self.law_data.columns),
                'sample': self.law_data.head(1).to_dict('records')[0] if len(self.law_data) > 0 else {}
            }
        
        if self.case_law_data is not None:
            info['case_law'] = {
                'records': len(self.case_law_data),
                'columns': list(self.case_law_data.columns),
                'sample': self.case_law_data.head(1).to_dict('records')[0] if len(self.case_law_data) > 0 else {}
            }
        
        return info
    
    def get_case_with_laws(self, case_id: int = None) -> pd.DataFrame:
        """
        Lấy thông tin bản án kèm các điều luật được áp dụng
        
        Args:
            case_id: ID của bản án cụ thể, nếu None thì lấy tất cả
            
        Returns:
            DataFrame với thông tin bản án và điều luật
        """
        if self.case_data is None or self.case_law_data is None:
            print("❌ Chưa load dữ liệu. Hãy gọi load_all_data() trước.")
            return pd.DataFrame()
        
        # Merge case với case_law
        merged = pd.merge(
            self.case_data,
            self.case_law_data,
            left_on='id',
            right_on='case_id',
            how='inner'
        )
        
        # Merge với law để lấy thông tin điều luật
        if self.law_data is not None:
            merged = pd.merge(
                merged,
                self.law_data,
                left_on='law_id',
                right_on='id',
                how='left',
                suffixes=('', '_law')
            )
        
        if case_id is not None:
            merged = merged[merged['id'] == case_id]
        
        return merged
    
    def get_law_statistics(self) -> Dict:
        """Thống kê về việc sử dụng các điều luật"""
        if self.case_law_data is None:
            return {}
        
        stats = {}
        
        # Thống kê theo điều luật
        law_counts = self.case_law_data['law_id'].value_counts()
        stats['law_usage'] = law_counts.to_dict()
        
        # Thống kê theo loại điều luật
        if 'type' in self.case_law_data.columns:
            type_counts = self.case_law_data['type'].value_counts()
            stats['type_usage'] = type_counts.to_dict()
        
        # Thống kê theo khoản, điểm
        if 'clause' in self.case_law_data.columns:
            clause_counts = self.case_law_data['clause'].value_counts()
            stats['clause_usage'] = clause_counts.to_dict()
        
        if 'point' in self.case_law_data.columns:
            point_counts = self.case_law_data['point'].value_counts()
            stats['point_usage'] = point_counts.to_dict()
        
        return stats
    
    def get_case_statistics(self) -> Dict:
        """Thống kê về bản án"""
        if self.case_data is None:
            return {}
        
        stats = {}
        
        # Thống kê theo loại tòa án
        if 'court_name' in self.case_data.columns:
            court_counts = self.case_data['court_name'].value_counts()
            stats['court_distribution'] = court_counts.to_dict()
        
        # Thống kê theo cấp độ
        if 'case_level' in self.case_data.columns:
            level_counts = self.case_data['case_level'].value_counts()
            stats['level_distribution'] = level_counts.to_dict()
        
        # Thống kê theo loại văn bản
        if 'document_type' in self.case_data.columns:
            doc_counts = self.case_data['document_type'].value_counts()
            stats['document_type_distribution'] = doc_counts.to_dict()
        
        return stats
    
    def search_cases(self, keyword: str, column: str = 'text') -> pd.DataFrame:
        """
        Tìm kiếm bản án theo từ khóa
        
        Args:
            keyword: Từ khóa tìm kiếm
            column: Cột để tìm kiếm (mặc định là 'text')
            
        Returns:
            DataFrame chứa các bản án thỏa mãn
        """
        if self.case_data is None:
            return pd.DataFrame()
        
        if column not in self.case_data.columns:
            print(f"❌ Cột '{column}' không tồn tại")
            return pd.DataFrame()
        
        # Tìm kiếm không phân biệt hoa thường
        mask = self.case_data[column].str.contains(keyword, case=False, na=False)
        results = self.case_data[mask]
        
        print(f"🔍 Tìm thấy {len(results)} bản án chứa từ khóa '{keyword}'")
        return results
    
    def get_law_by_id(self, law_id: int) -> Dict:
        """Lấy thông tin điều luật theo ID"""
        if self.law_data is None:
            return {}
        
        law = self.law_data[self.law_data['id'] == law_id]
        if len(law) > 0:
            return law.iloc[0].to_dict()
        return {}
    
    def get_case_by_id(self, case_id: int) -> Dict:
        """Lấy thông tin bản án theo ID"""
        if self.case_data is None:
            return {}
        
        case = self.case_data[self.case_data['id'] == case_id]
        if len(case) > 0:
            return case.iloc[0].to_dict()
        return {}


def main():
    """Test function"""
    loader = DataLoader()
    data = loader.load_all_data()
    
    print("\n📊 THÔNG TIN DỮ LIỆU:")
    print("=" * 50)
    
    info = loader.get_data_info()
    for table_name, table_info in info.items():
        print(f"\n📋 {table_name.upper()}:")
        print(f"  - Số records: {table_info['records']:,}")
        print(f"  - Số cột: {len(table_info['columns'])}")
        print(f"  - Các cột: {', '.join(table_info['columns'])}")
    
    # Thống kê
    print("\n📈 THỐNG KÊ:")
    print("=" * 50)
    
    law_stats = loader.get_law_statistics()
    if law_stats:
        print(f"\n📜 Thống kê điều luật:")
        if 'law_usage' in law_stats:
            print(f"  - Top 5 điều luật được sử dụng nhiều nhất:")
            top_laws = sorted(law_stats['law_usage'].items(), key=lambda x: x[1], reverse=True)[:5]
            for law_id, count in top_laws:
                print(f"    + Điều luật {law_id}: {count} lần")
    
    case_stats = loader.get_case_statistics()
    if case_stats:
        print(f"\n📄 Thống kê bản án:")
        if 'court_distribution' in case_stats:
            print(f"  - Phân bố theo tòa án:")
            for court, count in list(case_stats['court_distribution'].items())[:5]:
                print(f"    + {court}: {count} bản án")


if __name__ == "__main__":
    main() 