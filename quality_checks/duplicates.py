import pandas as pd

def check_duplicates(df):
    """Check for duplicate rows in the dataframe"""
    # Full duplicates
    full_duplicates = df.duplicated()
    full_dup_count = full_duplicates.sum()
    
    # Check for column-wise duplicates
    column_duplicates = {}
    for col in df.columns:
        dup_values = df[col][df[col].duplicated()].unique()
        if len(dup_values) > 0:
            column_duplicates[col] = {
                'count': len(dup_values),
                'examples': dup_values[:3].tolist() if len(dup_values) > 0 else []
            }
    
    # Most common duplicate combinations
    result = {
        'full_duplicate_count': full_dup_count,
        'full_duplicate_percent': round(full_dup_count / len(df) * 100, 2) if len(df) > 0 else 0,
        'column_duplicates': column_duplicates
    }
    
    return result