import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import httpx
import chardet

# Constants
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN", "").strip()

# Validate API token
if not AIPROXY_TOKEN:
    print("Error: API token is required.")
    sys.exit(1)

# Utility Functions
def load_data(file_path):
    """Load CSV data with encoding detection."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result.get('encoding', 'utf-8')
    return pd.read_csv(file_path, encoding=encoding)

def analyze_data(df):
    """Perform generic data analysis."""
    if df.empty:
        raise ValueError("The dataset is empty.")
    numeric_df = df.select_dtypes(include=['number'])
    return {
        'summary': df.describe(include='all', datetime_is_numeric=True).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'correlation': numeric_df.corr().to_dict() if not numeric_df.empty else {}
    }

def visualize_data(df, output_dir):
    """Generate visualizations and save PNG files in output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    sns.set(style="whitegrid")
    numeric_columns = df.select_dtypes(include=['number']).columns
    visualizations = []

    # Distribution plots
    for column in numeric_columns[:4]:  # Limit to 4 plots
        plt.figure()
        sns.histplot(df[column].dropna(), kde=True)
        plt.title(f'Distribution of {column}')
        filename = os.path.join(output_dir, f'{column}_distribution.png')
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        plt.close()
        visualizations.append(filename)

    # Heatmap
    if len(numeric_columns) > 1:
        plt.figure(figsize=(8, 6))
        correlation_matrix = df[numeric_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Heatmap")
        filename = os.path.join(output_dir, 'correlation_heatmap.png')
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        plt.close()
        visualizations.append(filename)

    return visualizations

def generate_narrative(analysis, visualizations):
    """Generate a narrative based on analysis."""
    headers = {
        'Authorization': f'Bearer {AIPROXY_TOKEN}',
        'Content-Type': 'application/json'
    }
    prompt = (
        f"The data analysis revealed the following insights:\n"
        f"Summary Statistics: {analysis['summary']}\n"
        f"Missing Values: {analysis['missing_values']}\n"
        f"Correlation Matrix: {analysis['correlation']}\n"
        f"Visualizations: {visualizations}.\n"
        "Write a comprehensive analysis and actionable insights."
    )
    data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
    response = httpx.post(API_URL, headers=headers, json=data, timeout=30.0)
    response.raise_for_status()
    return response.json().get('choices', [{}])[0].get('message', {}).get('content', "No response.")

def main(dataset_name):
    dataset_path = f"{dataset_name}.csv"
    output_dir = dataset_name
    df = load_data(dataset_path)
    analysis = analyze_data(df)
    visualizations = visualize_data(df, output_dir)
    narrative = generate_narrative(analysis, visualizations)

    # Save narrative to README.md
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, 'w') as f:
        f.write(narrative)

if _name_ == "_main_":
    datasets = ["goodreads", "happiness", "media"]
    for dataset in datasets:
        try:
            main(dataset)
        except Exception as e:
            print(f"Error processing {dataset}: {e}")
