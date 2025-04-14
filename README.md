# Data Quality Assessment Tool

![Data Quality Banner](https://img.shields.io/badge/Data%20Quality-Assessment%20Tool-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0.3-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

A powerful web application for quickly assessing data quality issues in datasets. This tool automatically identifies missing values, outliers, data type inconsistencies, and duplicate records, helping data professionals save time and improve data reliability.

![Screenshot](images/dqa_ss_1.png)
![Screenshot](images/dqa_ss_2.png)
![Screenshot](images/dqa_ss_3.png)
![Screenshot](images/dqa_ss_4.png)

## 🌟 Features

- **Comprehensive Quality Analysis**
  - Missing value detection and visualization
  - Outlier identification using statistical methods
  - Data type consistency validation
  - Duplicate record detection

- **Interactive Visualizations**
  - Visual representation of data quality issues
  - Dynamic charts showing data distribution
  - Clear indicators of problematic areas

- **Flexible Input Support**
  - CSV file support
  - Excel file compatibility
  - JSON data processing

- **Detailed Reporting**
  - Downloadable quality reports
  - Actionable insights for data cleaning
  - Summarized quality metrics

## 📋 Installation

1. **Clone the repository**

```bash
git clone https://github.com/godwinwa/data-quality-app.git
cd data-quality-assessment-tool

Create and activate a virtual environment

bashpython -m venv dqa-env
source dqa-env/bin/activate  # On Windows: dqa-env\Scripts\activate

Install dependencies

bashpip install -r requirements.txt

Run the application

bashpython app.py

Access the tool

Open your browser and go to: http://localhost:5000
🚀 Usage

Upload your dataset

Click the "Upload" button on the homepage
Select a CSV, Excel, or JSON file
Click "Analyze Data"


Review the analysis

Examine the summary statistics
Explore interactive visualizations
Review detailed quality issues by category


Export results

Download the complete quality report
Use insights to clean and improve your data



📊 Data Quality Checks
Missing Values Analysis

- Identifies columns with missing data
- Calculates the percentage of missing values in each field
- Highlights fields requiring data completion

Outlier Detection

- Uses statistical methods (IQR or Z-score)
- Identifies numerical values that significantly deviate from the norm
- Provides visual representation of outlier distribution

Data Type Consistency

- Validates that data conforms to expected types
- Identifies potential type mismatches or conversion opportunities
- Suggests appropriate data type transformations

Duplicate Detection

- Finds exact duplicate records
- Highlights columns with high duplication rates
- Calculates duplication percentages across the dataset

🔧 Technical Architecture

Backend: Flask web framework
Data Processing: Pandas, NumPy
Visualization: Plotly
Frontend: Bootstrap, HTML/CSS/JavaScript

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
📬 Contact
Have questions or suggestions? Feel free to reach out!

Made with ❤️ by G
