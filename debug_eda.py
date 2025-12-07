# debug_eda.py
# Adds src/ to Python path so we can import data_utils, then saves three EDA plots.
from pathlib import Path
import sys

# Ensure src/ is on the module search path so "from data_utils import ..." works
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import seaborn as sns
import matplotlib
matplotlib.use("Agg")   # non-interactive backend for saving figures
import matplotlib.pyplot as plt

from data_utils import load_datasets

def main():
    out = Path("reports/figures")
    out.mkdir(parents=True, exist_ok=True)

    print("OUTDIR ->", out.resolve())

    df = load_datasets("data")
    print("DF shape ->", df.shape)
    print("Columns ->", df.columns.tolist())

    # 1) G3 distribution
    f1 = out / "g3_dist.png"
    plt.figure(figsize=(6,4))
    sns.histplot(df["G3"], bins=20, kde=True)
    plt.title("Final grade (G3) distribution")
    plt.savefig(f1)
    plt.close()
    print("Saved g3_dist ->", f1.resolve(), "Exists?", f1.exists())

    # 2) Numeric correlation heatmap
    numeric = df.select_dtypes(include="number")
    corr = numeric.corr()
    f2 = out / "corr_numeric.png"
    plt.figure(figsize=(12,10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Numeric feature correlations")
    plt.savefig(f2)
    plt.close()
    print("Saved corr_numeric ->", f2.resolve(), "Exists?", f2.exists())

    # 3) Studytime vs G3 scatter
    f3 = out / "studytime_vs_g3.png"
    plt.figure(figsize=(6,4))
    sns.scatterplot(x="studytime", y="G3", data=df, alpha=0.6)
    plt.title("Studytime vs G3")
    plt.savefig(f3)
    plt.close()
    print("Saved studytime_vs_g3 ->", f3.resolve(), "Exists?", f3.exists())

    # Final listing
    print("\nFinal folder listing:")
    for fn in sorted(out.glob("*")):
        print("-", fn.name)

if __name__ == "__main__":
    main()
