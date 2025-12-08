import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("Dataset/student_performance_portuguese_dataset.csv")   # change filename if needed

print(df.head())
print(df.info())
print(df.describe())
print(df.isna().sum())

# 1. Histogram for numeric columns 
df.hist(figsize=(12, 8), bins=30)
plt.tight_layout()
plt.show()

# 2. Boxplots for numeric columns 
numeric_cols = df.select_dtypes(include='number').columns

plt.figure(figsize=(12, 6))
df[numeric_cols].boxplot()
plt.title("Boxplot of Numeric Columns")
plt.xticks(rotation=45)
plt.show()

# 3. Correlation Heatmap 
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
