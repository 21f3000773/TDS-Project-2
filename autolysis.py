import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
from io import StringIO

def main():
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <dataset.csv>")
        sys.exit(1)

    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)

    # Load dataset
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading the file: {e}")
        sys.exit(1)

    # Basic dataset overview
    summary = {
        "Shape": data.shape,
        "Columns": data.dtypes.to_dict(),
        "Missing Values": data.isnull().sum().to_dict(),
        "Sample Data": data.head().to_dict(),
    }

    # Generate correlation matrix if numeric data exists
    correlation_file = "correlation_heatmap.png"
    if not data.select_dtypes(include=['number']).empty:
        correlation_matrix = data.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.savefig(correlation_file)
        plt.close()
    else:
        correlation_file = None

    # Initialize OpenAI API
    openai.api_key = os.environ.get("AIPROXY_TOKEN")
    if not openai.api_key:
        print("Error: AIPROXY_TOKEN environment variable is not set.")
        sys.exit(1)

    # Send dataset summary to LLM
    summary_text = (f"Dataset Summary:\nShape: {summary['Shape']}\n"
                    f"Columns: {summary['Columns']}\n"
                    f"Missing Values: {summary['Missing Values']}\n"
                    f"Sample Data: {summary['Sample Data']}\n")

    # Use LLM for additional analysis suggestions
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data analysis assistant."},
            {"role": "user", "content": summary_text},
            {"role": "user", "content": "What additional analysis or visualizations should be performed on this dataset?"}
        ]
    )

    suggestions = response['choices'][0]['message']['content']

    # Save README.md
    readme_content = f"""
# Dataset Analysis Report

## Overview

### Dataset Summary

- **Shape:** {summary['Shape']}
- **Columns:** {summary['Columns']}
- **Missing Values:** {summary['Missing Values']}

### Sample Data

```
{data.head().to_string(index=False)}
```

## Visualizations

### Correlation Matrix

![Correlation Matrix]({correlation_file})

## Insights and Suggestions

{suggestions}

"""

    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

    print("Analysis complete. Files generated:")
    print("- README.md")
    if correlation_file:
        print(f"- {correlation_file}")

if __name__ == "__main__":
    main()
