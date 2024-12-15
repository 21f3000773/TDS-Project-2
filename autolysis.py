# /// script
# requires-python = ">=3.11"
# dependencies = [
<<<<<<< HEAD
#   "seaborn",
#   "pandas",
#   "matplotlib",
#   "httpx",
#   "chardet",
#   "numpy",
#   "requests",
=======
#   "pandas",
#   "seaborn",
#   "matplotlib",
#   "httpx",
#   "openai",
#   "python-dotenv",
>>>>>>> e46eabb0b3331721d7671bdc097a0e1ce74ed272
# ]
# ///

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
<<<<<<< HEAD
import seaborn as sns
import requests
import json
import chardet
=======
import openai
import httpx
>>>>>>> e46eabb0b3331721d7671bdc097a0e1ce74ed272

# Set OpenAI API key (Ensure it's set as an environment variable)
api_url = "https://api.openai.com/v1/models"  # Official OpenAI endpoint
headers = {
    "Authorization": f"Bearer {input('Enter your API key: ').strip()}",
    "Content-Type": "application/json"
}

<<<<<<< HEAD
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


def generate_summary(df):
    """Generate a summary of the dataset."""
    summary = {
        "shape": df.shape,
        "columns": [
            {"name": col, "type": str(df[col].dtype), "examples": df[col].dropna().unique()[:5].tolist()}
            for col in df.columns
        ],
        "missing_values": df.isnull().sum().to_dict(),
        "summary_statistics": df.describe(include='all').to_dict(),
=======
try:
    response = httpx.get(api_url, headers=headers, timeout=10)
    response.raise_for_status()
    print("Authentication successful:", response.json())
except httpx.HTTPStatusError as e:
    print(f"Authentication failed: {e}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")

def load_data(file_path):
    """Load CSV data and handle encoding issues."""
    try:
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 decoding failed, trying 'ISO-8859-1'")
        return pd.read_csv(file_path, encoding='ISO-8859-1')

def analyze_data(data):
    """Perform basic dataset analysis."""
    numeric_data = data.select_dtypes(include=['number'])
    analysis = {
        "Shape": data.shape,
        "Columns": data.dtypes.to_dict(),
        "Missing Values": data.isnull().sum().to_dict(),
        "Sample Data": data.head().to_dict(),
        "Correlation Matrix": numeric_data.corr().to_dict() if not numeric_data.empty else None
>>>>>>> e46eabb0b3331721d7671bdc097a0e1ce74ed272
    }
    return summary

<<<<<<< HEAD
def visualize_data(df):
    """Generate visualizations and save them as PNG files."""
    output_files = []

    # Correlation heatmap for numeric columns
    numeric_cols = df.select_dtypes(include=['number'])
    if not numeric_cols.empty:
        plt.figure(figsize=(6, 6))  # Adjust dimensions to 512x512 px
        corr_matrix = numeric_cols.corr()
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
        heatmap_file = "correlation_heatmap.png"
        plt.title("Correlation Heatmap")
        plt.savefig(heatmap_file, dpi=100)
        plt.close()
        output_files.append(heatmap_file)

    # Distribution plots for up to 2 numeric columns
    for i, col in enumerate(numeric_cols.columns[:2]):
        plt.figure(figsize=(6, 6))  # Adjust dimensions to 512x512 px
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f"Distribution of {col}")
        dist_file = f"{col}_distribution.png"
        plt.savefig(dist_file, dpi=100)
        plt.close()
        output_files.append(dist_file)

    return output_files

def query_llm(prompt, token):
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
    summary = generate_summary(df)

    # Query LLM for analysis and storytelling
    prompt = (
        "Here is a summary of a dataset:\n" +
        f"The dataset contains {summary['shape'][0]} rows and {summary['shape'][1]} columns.\n" +
        "Column details and missing values are as follows:\n" +
        "\n".join([f"- {col['name']} ({col['type']}): {col['examples']} examples; {summary['missing_values'][col['name']]} missing values" for col in summary['columns']]) +
        "\nPlease analyze this dataset and provide insights as a story."
    )
    insights = query_llm(prompt, token)

    # Visualize data
    output_files = visualize_data(df)

    # Write README.md
    write_readme(summary, prompt, insights, output_files)
    print("Analysis complete. README.md and visualizations generated.")

=======
def visualize_data(data):
    """Create and save visualizations."""
    numeric_data = data.select_dtypes(include=['number'])
    if not numeric_data.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.savefig('correlation_heatmap.png')
        plt.close()
        return 'correlation_heatmap.png'
    return None

def generate_narrative(analysis):
    """Generate insights using OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data analysis assistant."},
                {"role": "user", "content": f"Analyze the dataset with the following details: {analysis}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred while generating insights: {e}"

def save_report(analysis, visualization_file, narrative):
    """Save the analysis and narrative into README.md."""
    with open("README.md", "w") as file:
        file.write(f"""
# Dataset Analysis Report

## Overview

### Dataset Summary

- **Shape:** {analysis['Shape']}
- **Columns:** {analysis['Columns']}
- **Missing Values:** {analysis['Missing Values']}

### Sample Data

```
{pd.DataFrame(analysis['Sample Data']).to_string(index=False)}

```

## Visualizations

### Correlation Matrix

{f"![Correlation Matrix]({visualization_file})" if visualization_file else "No numeric data available for visualization."}

## Insights and Suggestions

{narrative}
""")
    print("README.md file created.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    data = load_data(file_path)
    analysis = analyze_data(data)
    visualization_file = visualize_data(data)
    narrative = generate_narrative(analysis)
    save_report(analysis, visualization_file, narrative)
    print("Analysis complete. Files generated:")
    print("- README.md")
    if visualization_file:
        print(f"- {visualization_file}")

>>>>>>> e46eabb0b3331721d7671bdc097a0e1ce74ed272
if __name__ == "__main__":
    main()
