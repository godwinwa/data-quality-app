# app.py
print(">>> app.py is running")

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import pandas as pd
import json
import io
import uuid
import os
import tempfile
from datetime import datetime

# Import our modules
from quality_checks.missing_values import analyze_missing_values
from quality_checks.outliers import detect_outliers
from quality_checks.data_types import check_data_types
from quality_checks.duplicates import check_duplicates
from utils.data_loader import load_data
from utils.report_generator import generate_full_report
from utils.numpy_utils import convert_numpy_types

# Add this class for handling NumPy types in JSON serialization
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = NumpyEncoder
app.secret_key = os.environ.get('SECRET_KEY', str(uuid.uuid4()))

# Configure server-side sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# Create a temporary directory to store uploaded files
UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    try:
        # Load the data
        df = load_data(file)
        
        # Store a sample in the session for display
        session['sample_data'] = df.head(5).to_html(classes='table table-striped')
        
        # Run quality checks
        missing_summary = analyze_missing_values(df)
        outliers_data = detect_outliers(df)
        type_summary, type_issues = check_data_types(df)
        duplicate_data = check_duplicates(df)
        
        # Generate the full report
        report = generate_full_report(
            df, 
            missing_summary, 
            outliers_data, 
            type_summary, 
            type_issues, 
            duplicate_data
        )
        
        # Convert NumPy types to native Python types before storing in session
        session['report'] = convert_numpy_types(report)
        session['filename'] = file.filename
        
        return redirect(url_for('results'))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results')
def results():
    if 'report' not in session:
        return redirect(url_for('index'))
        
    return render_template(
        'results.html',
        report=session['report'],
        sample_data=session.get('sample_data'),
        filename=session.get('filename')
    )

@app.route('/download_report')
def download_report():
    if 'report' not in session:
        return redirect(url_for('index'))
        
    # Create a simplified version for download
    download_report = {k: v for k, v in session['report'].items() if k != 'visualizations'}
    
    # Ensure all NumPy types are converted
    download_report = convert_numpy_types(download_report)
    
    response = jsonify(download_report)
    response.headers.set('Content-Disposition', 'attachment', filename=f'data-quality-report-{datetime.now().strftime("%Y%m%d%H%M%S")}.json')
    return response

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
