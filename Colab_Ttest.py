import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import numpy as np

# Load the new dataset (replace with the actual path to your data)
file_path = '/content/report_pg_matrix_log2.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Step 1: Define the 'C' and 'E' sample groups
c_samples = ['C1', 'C2', 'C3']
e_samples = ['E1', 'E2', 'E3']

# Step 2: Ensure all values in C and E groups are numeric, coercing non-numeric to NaN
df[c_samples + e_samples] = df[c_samples + e_samples].apply(pd.to_numeric, errors='coerce')

# Step 3: Filter rows where all 6 data points (3 per group) are non-NaN (100% completeness)
df['C_non_NaN'] = df[c_samples].notna().sum(axis=1)
df['E_non_NaN'] = df[e_samples].notna().sum(axis=1)

# Keep rows where both groups have 3 valid values
filtered_df = df[(df['C_non_NaN'] == 3) & (df['E_non_NaN'] == 3)].copy()

# Step 4: Calculate the mean for each condition
filtered_df['C_mean'] = filtered_df[c_samples].mean(axis=1)
filtered_df['E_mean'] = filtered_df[e_samples].mean(axis=1)

# Step 5: Calculate the difference between the two means
filtered_df['Mean_Difference'] = filtered_df['C_mean'] - filtered_df['E_mean']

# Step 6: Perform unpaired t-test between C and E for each row
def perform_ttest(row):
    c_values = row[c_samples].dropna().astype(float)
    e_values = row[e_samples].dropna().astype(float)
    return ttest_ind(c_values, e_values, nan_policy='omit').pvalue

# Apply t-test row-wise and store p-values in a new column
filtered_df['p_value'] = filtered_df.apply(perform_ttest, axis=1)

# Step 7: Apply Benjamini-Hochberg FDR correction for multiple comparisons
filtered_df['p_value_adj'] = multipletests(filtered_df['p_value'], method='fdr_bh')[1]

# Step 8: Add a "significance" column based on the adjusted p-value
alpha = 0.05  # Significance level
filtered_df['significance'] = np.where(filtered_df['p_value_adj'] < alpha, 'yes', 'no')

# Step 9: Combine metadata with results
# Assuming the first 4 columns of the source file are metadata columns (adjust if needed)
metadata_columns = df.columns[:4]
final_df = pd.concat([df[metadata_columns], 
                      filtered_df[['C_mean', 'E_mean', 'Mean_Difference', 'p_value', 'p_value_adj', 'significance']]], axis=1)

# Step 10: Save the results to a new Excel file
output_file_path = '/content/C_vs_E_TTest_Results_with_Metadata_And_Significance.xlsx'
final_df.to_excel(output_file_path, index=False)

print(f"Results with metadata, t-tests, and significance saved to: {output_file_path}")
