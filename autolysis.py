# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "seaborn",
#   "pandas",
#   "matplotlib",
#   "httpx",
#   "chardet",
#   "numpy",
#   "requests",
#   "scipy",
# ]
# ///

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import chardet
from scipy import stats

def load_csv(filename):
    """Load a CSV file and return a DataFrame."""
    try:
        # Detect file encoding
        with open(filename, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        
        # Load the CSV file with detected encoding
        df = pd.read_csv(filename, encoding=encoding)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def detect_outliers(df, method='zscore'):
    """Detect outliers using Z-score or IQR method."""
    numeric_cols = df.select_dtypes(include=['number'])
    outliers = {}

    if method == 'zscore':
        # Z-score method
        z_scores = stats.zscore(numeric_cols.fillna(0))
        outliers = (z_scores > 3).sum(axis=0)  # Z-score > 3 as outlier
    elif method == 'iqr':
        # IQR method
        Q1 = numeric_cols.quantile(0.25)
        Q3 = numeric_cols.quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((numeric_cols < (Q1 - 1.5 * IQR)) | (numeric_cols > (Q3 + 1.5 * IQR))).sum(axis=0)
    
    return outliers

def generate_summary(df, outlier_method='zscore'):
    """Generate a summary of the dataset with enhanced statistical insights."""
    summary = {
        "shape": df.shape,
        "columns": [
            {"name": col, "type": str(df[col].dtype), "examples": df[col].dropna().unique()[:5].tolist()}
            for col in df.columns
        ],
        "missing_values": df.isnull().sum().to_dict(),
        "summary_statistics": df.describe(include='all').to_dict(),
    }

    # Enhanced analysis: Outlier detection based on selected method
    numeric_cols = df.select_dtypes(include=['number'])

    if outlier_method == 'zscore':
        # Z-score calculation for outlier detection
        z_scores = stats.zscore(numeric_cols.fillna(0))
        outliers = (z_scores > 3).sum(axis=0)  # Consider Z-score > 3 as an outlier
        summary['outliers'] = {col: outliers[i] for i, col in enumerate(numeric_cols.columns)}
    
    elif outlier_method == 'iqr':
        # IQR for outlier detection
        Q1 = numeric_cols.quantile(0.25)
        Q3 = numeric_cols.quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = ((numeric_cols < (Q1 - 1.5 * IQR)) | (numeric_cols > (Q3 + 1.5 * IQR))).sum()
        summary['iqr_outliers'] = {col: iqr_outliers[col] for col in numeric_cols.columns}

    return summary


def visualize_data(df):
    """Generate visualizations and save them as PNG files."""
    output_files = []

    # Correlation heatmap for numeric columns
    numeric_cols = df.select_dtypes(include=['number'])
    if not numeric_cols.empty:
        plt.figure(figsize=(8, 8))  # Adjust dimensions to 512x512 px
        corr_matrix = numeric_cols.corr()
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Correlation coefficient'})
        plt.title("Correlation Heatmap of Numerical Columns")
        plt.savefig("correlation_heatmap.png", dpi=100)
        plt.close()
        output_files.append("correlation_heatmap.png")

        # Enhanced analysis: correlation significance
        for col1 in numeric_cols.columns:
            for col2 in numeric_cols.columns:
                if col1 != col2:
                    correlation, p_value = stats.pearsonr(df[col1].dropna(), df[col2].dropna())
                    if p_value < 0.05:
                        print(f"Significant correlation between {col1} and {col2}: {correlation:.2f}, p-value: {p_value:.4f}")
                    else:
                        print(f"Correlation between {col1} and {col2}: {correlation:.2f}, p-value: {p_value:.4f}")

    # Distribution plots for up to 2 numeric columns
    for i, col in enumerate(numeric_cols.columns[:2]):
        plt.figure(figsize=(6, 6))  # Adjust dimensions to 512x512 px
        sns.histplot(df[col], kde=True, bins=30, color="skyblue" if df[col].mean() > 0 else "salmon", label=col)
        plt.title(f"Distribution of {col}")
        plt.xlabel(f'{col} Values')
        plt.ylabel('Frequency')
        plt.legend(title=f"{col} Distribution", loc='upper right')
        dist_file = f"{col}_distribution.png"
        plt.savefig(dist_file, dpi=100)
        plt.close()
        output_files.append(dist_file)

    return output_files


def query_llm(prompt, token, analysis_results=None):
    """Query the GPT-4o-Mini LLM via AI Proxy and return the response."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are an expert data analyst."},
            {"role": "user", "content": prompt},
        ]
    }

    # Adjusting the prompt based on missing values or outliers if present
    if analysis_results and 'outliers' in analysis_results:
        prompt += "\nAdditionally, the dataset has outliers in the following columns:\n"
        for col, count in analysis_results['outliers'].items():
            if count > 0:
                prompt += f"- {col}: {count} potential outliers\n"

    api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error querying AI Proxy: {e}")
        sys.exit(1)

def write_readme(summary, analysis, insights, output_files):
    """Write the README.md file."""
    with open("README.md", "w") as f:
        f.write("# Automated Data Analysis Report\n\n")
        
        # Dataset Summary
        f.write("## Dataset Summary\n")
        f.write(f"The dataset contains {summary['shape'][0]} rows and {summary['shape'][1]} columns.\n\n")
        f.write("### Column Details:\n")
        for col in summary['columns']:
            f.write(f"- **{col['name']}** ({col['type']}): Example values: {col['examples']}\n")
        f.write("\n")
        
        f.write("### Missing Values:\n")
        for col, missing in summary['missing_values'].items():
            f.write(f"- {col}: {missing} missing values\n")
        f.write("\n")
        
        f.write("### Outliers Detected:\n")
        for col, count in summary['outliers'].items():
            if count > 0:
                f.write(f"- {col}: {count} potential outliers\n")
        f.write("\n")
        
        # Analysis and Insights
        f.write("## Analysis and Insights\n")
        f.write("### The Analysis\n")
        f.write(analysis)
        f.write("\n\n")

        f.write("### Insights\n")
        f.write(insights)
        f.write("\n\n")

        f.write("### Implications\n")
        f.write("Based on these insights, here are some potential actions or considerations:\n")
        f.write("- Explore specific outliers or trends highlighted in the analysis.\n")
        f.write("- Utilize identified correlations for predictive modeling or strategy formulation.\n")
        f.write("- Address missing or anomalous data to improve data quality.\n")
        f.write("\n\n")
        
        # Visualizations
        f.write("## Visualizations\n")
        for file in output_files:
            f.write(f"![{file}]({file})\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <dataset.csv>")
        sys.exit(1)

    filename = sys.argv[1]
    token = os.environ.get("AIPROXY_TOKEN")
    if not token:
        print("Error: AIPROXY_TOKEN environment variable not set.")
        sys.exit(1)

    # Load and summarize the dataset
    df = load_csv(filename)
    summary = generate_summary(df, outlier_method='iqr')  # Default outlier method changed to IQR

    # Query LLM for analysis and storytelling
    prompt = (
        "Here is a summary of a dataset:\n" +
        f"The dataset contains {summary['shape'][0]} rows and {summary['shape'][1]} columns.\n" +
        "Column details and missing values are as follows:\n" +
        "\n".join([f"- {col['name']} ({col['type']}): {col['examples']} examples; {summary['missing_values'][col['
