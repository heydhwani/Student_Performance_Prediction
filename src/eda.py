import os
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from data_utils import load_datasets

def run_eda():
    df = load_datasets("../data")
    out_dir = Path("../reports/figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Data shape:", df.shape)
    print(df.info())

    # 1. target distribution
    plt.figure(figsize=(6,4))
    sns.histplot(df["G3"], bins=20, kde=True)
    plt.title("Final grade (G3) distribution")
    plt.savefig(out_dir / "g3_dist.png")
    plt.close()

    # 2. numeric correlation heatmap
    numeric = df.select_dtypes(include="number")
    corr = numeric.corr()
    plt.figure(figsize=(12,10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Numeric feature correlations")
    plt.savefig(out_dir / "corr_numeric.png")
    plt.close()

    # 3. studytime vs G3 scatter
    plt.figure(figsize=(6,4))
    sns.scatterplot(x="studytime", y="G3", data=df, alpha=0.6)
    plt.title("Studytime vs G3")
    plt.savefig(out_dir / "studytime_vs_g3.png")
    plt.close()

    print("EDA figures saved to:", out_dir)

if __name__ == "__main__":
    run_eda()
