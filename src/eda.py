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