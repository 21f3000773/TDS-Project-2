# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "matplotlib",
# ]
# ///

import os
import pandas as pd
import matplotlib.pyplot as plt

def analyze_dataset(file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(file_path)

    # Generate README.md
    with open(os.path.join(output_dir, "README.md"), "w") as f:
        f.write(f"# Analysis of {os.path.basename(file_path)}\n\n")
        f.write(df.describe(include='all').to_string())

    # Generate visualizations
    for col in df.select_dtypes(include='number').columns:
        plt.figure()
        df[col].hist()
        plt.title(f"Histogram of {col}")
        plt.savefig(os.path.join(output_dir, f"{col}.png"))
        plt.close()

def main():
    datasets = {
        "goodreads.csv": "goodreads",
        "happiness.csv": "happiness",
        "media.csv": "media",
    }
    for file_path, output_dir in datasets.items():
        if os.path.exists(file_path):
            analyze_dataset(file_path, output_dir)

if __name__ == "_main_":
    main()
