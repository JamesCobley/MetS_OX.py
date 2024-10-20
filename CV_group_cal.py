import pandas as pd

# Load the dataset
file_path = '/content/report_pg_matrix_log2.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Assuming the structure: ['Protein.Group', 'C1', 'C2', 'C3', 'E1', 'E2', 'E3']
# Make sure to adjust column names if they are different

# Step 1: Calculate the CV for each protein group in each condition group (C1-C3, E1-E3)
# Group 1: C1, C2, C3
df['Mean_C'] = df[['C1', 'C2', 'C3']].mean(axis=1)
df['StdDev_C'] = df[['C1', 'C2', 'C3']].std(axis=1)
df['CV_C'] = (df['StdDev_C'] / df['Mean_C']) * 100  # Multiply by 100 to get percentage

# Group 2: E1, E2, E3
df['Mean_E'] = df[['E1', 'E2', 'E3']].mean(axis=1)
df['StdDev_E'] = df[['E1', 'E2', 'E3']].std(axis=1)
df['CV_E'] = (df['StdDev_E'] / df['Mean_E']) * 100  # Multiply by 100 to get percentage

# Step 2: Define the CV ranges
def categorize_cv(cv_value):
    if cv_value < 5:
        return '< 5%'
    elif cv_value < 10:
        return '< 10%'
    elif cv_value < 15:
        return '< 15%'
    elif cv_value < 20:
        return '< 20%'
    else:
        return '> 20%'

# Apply the categorization for both conditions
df['CV_Range_C'] = df['CV_C'].apply(categorize_cv)
df['CV_Range_E'] = df['CV_E'].apply(categorize_cv)

# Step 3: Calculate the percentage of proteins in each CV range for both groups
cv_range_counts_c = df['CV_Range_C'].value_counts(normalize=True) * 100  # Normalize to get percentage
cv_range_counts_e = df['CV_Range_E'].value_counts(normalize=True) * 100

# Step 4: Print the percentage of proteins in each CV range for both conditions
print("Percentage of Proteins in Each CV Range for Group C (C1-C3):")
print(cv_range_counts_c)

print("\nPercentage of Proteins in Each CV Range for Group E (E1-E3):")
print(cv_range_counts_e)

# Optional: Save the results to an Excel file for further analysis
output_file = '/content/CV_Analysis_Results.xlsx'
df.to_excel(output_file, index=False)
print(f"Results saved to {output_file}")
