import pandas as pd
import os
import io

def load_data(file_obj, file_type=None):
    """
    Load data from various file formats
    
    Parameters:
    -----------
    file_obj : file object or str
        The file object or path to load
    file_type : str, optional
        The type of file ('csv', 'excel', 'json')
        
    Returns:
    --------
    pandas.DataFrame
    """
    if file_type is None:
        # Try to infer file type from filename
        if hasattr(file_obj, 'filename'):
            filename = file_obj.filename.lower()
            if filename.endswith('.csv'):
                file_type = 'csv'
            elif filename.endswith(('.xls', '.xlsx')):
                file_type = 'excel'
            elif filename.endswith('.json'):
                file_type = 'json'
            else:
                raise ValueError("Unable to determine file type")
    
    # Load based on file type
    if file_type == 'csv':
        return pd.read_csv(file_obj)
    elif file_type == 'excel':
        return pd.read_excel(file_obj)
    elif file_type == 'json':
        return pd.read_json(file_obj)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")