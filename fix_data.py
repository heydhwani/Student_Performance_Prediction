from pathlib import Path
import pandas as pd
import csv

def detect_sep(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            sample = f.read(2048)
            return csv.Sniffer().sniff(sample).delimiter
    except:
        return ";"

def clean_file(in_path, out_path):
    sep = detect_sep(in_path)
    df = pd.read_csv(in_path, sep=sep, engine="python")

    # remove extra header rows
    cols = df.columns.tolist()
    df = df[df.apply(lambda r: not all(str(r[c])==str(cols[i]) for i,c in enumerate(df.columns)), axis=1)]

    # drop giant header column
    drop_cols = [c for c in df.columns if c.count(",") > 3]
    df = df.drop(columns=drop_cols, errors="ignore")

    # clean numeric columns
    numeric_cols = ['age','Medu','Fedu','traveltime','studytime','failures','famrel',
                    'freetime','goout','Dalc','Walc','health','absences','G1','G2','G3']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.to_csv(out_path, index=False)
    print(f"Fixed file saved to: {out_path}")

# Fix both CSVs
clean_file("data/student-mat.csv", "data/student-mat-clean.csv")
clean_file("data/student-por.csv", "data/student-por-clean.csv")
print("DONE.")
