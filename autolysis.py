# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "pandas",
#     "chardet",
#     "matplotlib",
#     "python-dotenv",
#     "rich",
#     "seaborn",
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import httpx
import chardet

# Constants
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = input("Please enter your API token: ").strip()

# Validate API token
if not AIPROXY_TOKEN:
    print("Error: API token is required.")
    sys.exit(1)

# Utility Functions
def load_data(file_path):
    """Load CSV data with encoding detection."""
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        sys.exit(1)
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result.get('encoding', 'utf-8')
        return pd.read_csv(file_path, encoding=encoding)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def analyze_data(df):
    """Perform generic data analysis."""
    if df.empty:
        print("Error: The dataset is empty.")
        sys.exit(1)
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        print("Error: No numeric columns found in the dataset.")
        sys.exit(1)
    return {
        'summary': df.describe(include='all', datetime_is_numeric=True).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'correlation': numeric_df.corr().to_dict(),
    }

def visualize_data(df):
    """Generate and save up to 5 visualizations, including a heatmap."""
    sns.set(style="whitegrid")
    numeric_columns = df.select_dtypes(include=['number']).columns
    if numeric_columns.empty:
        print("No numeric columns to visualize.")
        return []
    visualizations = []
    # Distribution plots (limit to 4)
    for i, column in enumerate(numeric_columns[:4]):
        plt.figure()
        sns.histplot(df[column].dropna(), kde=True)
        plt.title(f'Distribution of {column}')
        filename = f'{column}_distribution.png'
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        plt.close()
        visualizations.append(filename)
    # Heatmap for correlation (always include if possible)
    if len(numeric_columns) > 1:
        plt.figure(figsize=(8, 6))
        correlation_matrix = df[numeric_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Heatmap")
        heatmap_filename = "correlation_heatmap.png"
        plt.savefig(heatmap_filename, dpi=100, bbox_inches='tight')
        plt.close()
        visualizations.append(heatmap_filename)
    return visualizations

def generate_narrative(analysis, visualizations):
    """Generate a story based on the analysis using LLM."""
    headers = {
        'Authorization': f'Bearer {AIPROXY_TOKEN}',
        'Content-Type': 'application/json'
    }
    prompt = (
        f"The data analysis revealed the following insights:\n"
        f"Summary Statistics: {analysis['summary']}\n"
        f"Missing Values: {analysis['missing_values']}\n"
        f"Correlation Matrix: {analysis['correlation']}\n"
        f"Additionally, the following visualizations were created: {visualizations}.\n"
        "Based on this information, write a comprehensive analysis and provide actionable insights."
    )
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = httpx.post(API_URL, headers=headers, json=data, timeout=30.0)
        response.raise_for_status()
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', "No response content.")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return "Narrative generation failed due to an error."

def main(file_path):
    try:
        df = load_data(file_path)
        analysis = analyze_data(df)
        visualizations = visualize_data(df)
        narrative = generate_narrative(analysis, visualizations)
        with open('README.md', 'w') as f:
            f.write(narrative)
            if "correlation_heatmap.png" in visualizations and os.path.exists("correlation_heatmap.png"):
                f.write("\n\n![Correlation Heatmap](correlation_heatmap.png)")
            else:
                print("Correlation heatmap not found, skipping embedding in README.")
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        sys.exit(1)

if _name_ == "_main_":
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)
    main(sys.argv[1])
