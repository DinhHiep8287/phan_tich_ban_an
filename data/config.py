"""
Cấu hình cho dự án gán nhãn điều luật
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3307)),  # Port thực tế của bạn
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Dinhhiep123'),
    'database': os.getenv('DB_NAME', 'my_database'),  # Database thực tế của bạn
    'charset': 'utf8mb4'
}

# Law types mapping
LAW_TYPES = {
    'BLHS': 'hình sự',
    'BLTTHS': 'tố tụng hình sự', 
    'BLTHAHS': 'thi hành án hình sự'
}

# Law name variations
LAW_VARIATIONS = {
    'Bộ luật hình sự': ['BLHS', 'BLHS 2015', 'bộ luật hình sự 2015', 
                        'bộ luật hình sự 2015 (sửa đổi bổ sung 2017)'],
    'Bộ luật tố tụng hình sự': ['BLTTHS', 'bộ luật tố tụng hình sự 2015'],
    'Bộ luật thi hành án hình sự': ['BLTHAHS']
}

# Regex patterns for law extraction
LAW_PATTERNS = {
    'article': r'điều\s+(\d+)',
    'clause': r'khoản\s+(\d+)',
    'point': r'điểm\s+([a-z])',
    'law_type': r'(BLHS|BLTTHS|BLTHAHS|bộ luật hình sự|bộ luật tố tụng hình sự|bộ luật thi hành án hình sự)'
}

# Model parameters
MODEL_CONFIG = {
    'tfidf': {
        'max_features': 10000,
        'ngram_range': (1, 2),
        'min_df': 2
    },
    'bm25': {
        'k1': 1.5,
        'b': 0.75
    }
}

# Evaluation parameters
EVAL_CONFIG = {
    'k_values': list(range(5, 201, 5)),  # k từ 5 đến 200, bước 5
    'metrics': ['precision', 'recall', 'f1', 'map', 'mar']
} 