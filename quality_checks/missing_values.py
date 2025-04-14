import pandas as pd
import numpy as np

def analyze_missing_values(df):
    """Analyze missing values in the dataframe"""
    # Calculate missing values
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df) * 100).round(2)
    
    # Create a summary dataframe
    missing_summary = pd.DataFrame({
        'column': df.columns,
        'missing_count': missing_count.values,
        'missing_percent': missing_percent.values
    })
    
    # Sort by missing percent
    missing_summary = missing_summary.sort_values('missing_percent', ascending=False)
    
    return missing_summary
