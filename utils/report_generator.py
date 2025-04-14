import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
from utils.numpy_utils import convert_numpy_types

def generate_summary_stats(df):
    """Generate basic summary statistics for a dataframe"""
    # Basic stats
    stats = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
    }
    
    # Data types summary
    dtypes = df.dtypes.value_counts().to_dict()
    stats['data_types'] = {str(k): int(v) for k, v in dtypes.items()}
    
    return stats

def create_missing_values_plot(missing_summary):
    """Create visualization for missing values"""
    if missing_summary.empty:
        return None
    
    # Only include columns with missing values
    missing_summary = missing_summary[missing_summary['missing_count'] > 0]
    
    if missing_summary.empty:
        return None
    
    fig = px.bar(
        missing_summary, 
        x='column', 
        y='missing_percent',
        title='Missing Values by Column (%)',
        labels={'column': 'Column', 'missing_percent': 'Missing (%)'},
        color='missing_percent',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'},
        height=400
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def create_outliers_plot(outliers_data, df):
    """Create visualization for outliers"""
    if not outliers_data:
        return None
    
    # Prepare data for plotting
    plot_data = []
    for col, data in outliers_data.items():
        plot_data.append({
            'column': col,
            'outlier_percent': data['percent']
        })
    
    outlier_df = pd.DataFrame(plot_data)
    
    if outlier_df.empty:
        return None
    
    fig = px.bar(
        outlier_df,
        x='column',
        y='outlier_percent',
        title='Outliers by Column (%)',
        labels={'column': 'Column', 'outlier_percent': 'Outliers (%)'},
        color='outlier_percent',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'},
        height=400
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def generate_full_report(df, missing_summary, outliers_data, type_summary, type_issues, duplicate_data):
    """Generate a comprehensive data quality report"""
    report = {
        'summary': generate_summary_stats(df),
        'missing_values': missing_summary.to_dict(orient='records') if not missing_summary.empty else [],
        'outliers': outliers_data,
        'data_types': type_summary.to_dict(orient='records'),
        'type_issues': type_issues,
        'duplicates': duplicate_data,
        'visualizations': {
            'missing_values': create_missing_values_plot(missing_summary),
            'outliers': create_outliers_plot(outliers_data, df)
        }
    }
    
    # Convert NumPy types to native Python types before returning
    return convert_numpy_types(report)