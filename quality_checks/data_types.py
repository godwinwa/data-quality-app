import pandas as pd
import numpy as np
import re

def check_data_types(df):
    """Analyze data types and potential mismatches"""
    
    # Fix for the first sampling issue
    def safe_sample(series, n):
        # Make sure we don't sample more elements than available
        non_na_count = series.dropna().shape[0]
        if non_na_count == 0:
            return []
        safe_n = min(n, non_na_count)
        return series.dropna().sample(safe_n).tolist() if safe_n > 0 else []
    
    type_summary = pd.DataFrame({
        'column': df.columns,
        'dtype': df.dtypes.astype(str),
        'unique_values': [df[col].nunique() for col in df.columns],
        'samples': [str(safe_sample(df[col], 3)) for col in df.columns]
    })
    
    # Check for potential type mismatches
    type_issues = []
    
    for col in df.columns:
        # Current type
        curr_type = df[col].dtype
        
        # Skip columns with all missing values
        if df[col].isnull().all():
            continue
        
        # Fix for the second sampling issue
        non_na_count = df[col].dropna().shape[0]
        safe_sample_size = min(10, non_na_count)
        sample_vals = df[col].dropna().sample(safe_sample_size).tolist() if safe_sample_size > 0 else []
        
        # Check if string column might be datetime
        if curr_type == 'object' and len(sample_vals) > 0:
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{2}-\d{2}-\d{4}'   # DD-MM-YYYY
            ]
            
            sample = str(sample_vals[:min(3, len(sample_vals))])
            for pattern in date_patterns:
                if re.search(pattern, sample):
                    type_issues.append({
                        'column': col,
                        'current_type': str(curr_type),
                        'suggested_type': 'datetime',
                        'reason': f"Contains date-like patterns: {sample}"
                    })
                    break
        
        # Check if numeric strings
        if curr_type == 'object' and len(sample_vals) > 0:
            # Try to convert a sample to numeric
            try:
                safe_sample_size = min(5, non_na_count)
                if safe_sample_size > 0:
                    numeric_sample = pd.to_numeric(df[col].dropna().sample(safe_sample_size))
                    type_issues.append({
                        'column': col,
                        'current_type': str(curr_type),
                        'suggested_type': 'numeric',
                        'reason': f"Contains numeric-like values: {sample_vals[:min(3, len(sample_vals))]}"
                    })
            except:
                pass
    
    return type_summary, type_issues