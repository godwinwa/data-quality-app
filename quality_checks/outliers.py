import pandas as pd
import numpy as np

def detect_outliers(df, method='iqr', threshold=1.5):
    """Detect outliers in numeric columns using IQR or Z-score method"""
    numeric_cols = df.select_dtypes(include=np.number).columns
    result = {}
    
    for col in numeric_cols:
        # Skip columns with all missing values
        if df[col].isnull().all():
            continue
            
        if method == 'iqr':
            # IQR method
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        else:
            # Z-score method
            mean = df[col].mean()
            std = df[col].std()
            z_scores = abs((df[col] - mean) / std)
            outliers = df[z_scores > threshold][col]
        
        if not outliers.empty:
            result[col] = {
                'count': len(outliers),
                'percent': round(len(outliers) / len(df) * 100, 2),
                'min': outliers.min() if not outliers.empty else None,
                'max': outliers.max() if not outliers.empty else None
            }
    
    return result