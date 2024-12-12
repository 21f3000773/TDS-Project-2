# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "seaborn",
#   "matplotlib",
#   "httpx",
#   "openai",
#   "python-dotenv",
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
import httpx

# Set OpenAI API key (Ensure it's set as an environment variable)
api_url = "https://api.openai.com/v1/models"  # Official OpenAI endpoint
headers = {
    "Authorization": f"Bearer {input('Enter your API key: ').strip()}",
    "Content-Type": "application/json"
}

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
    }
    return analysis

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

if __name__ == "__main__":
    main()
