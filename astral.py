import pandas as pd

# Load the Excel file
file_path = '/content/Astral_Exp_James_1.xlsx'
df = pd.read_excel(file_path)

# Specify the columns that correspond to samples ending with .dia
sample_columns = [
    'X:\\H_James\\James\\James_HeLaOXC_30SPD_250ng_120924_S3.raw.dia',
    'X:\\H_James\\James\\James_HeLaOXC_30SPD_250ng_120924_S9.raw.dia',
    'X:\\H_James\\James\\James_HeLaOXC_30SPD_250ng_120924_S15.raw.dia',
    'X:\\H_James\\James\\James_HeLaOXE_30SPD_250ng_120924_S4.raw.dia',
    'X:\\H_James\\James\\James_HeLaOXE_30SPD_250ng_120924_S10.raw.dia',
    'X:\\H_James\\James\\James_HeLaOXE_30SPD_250ng_120924_S16.raw.dia'
]

# Dictionary to store results
unique_protein_counts = {}

# Loop through each sample column to count unique protein groups
for sample in sample_columns:
    # Extract rows where the current sample column is not blank
    sample_df = df[df[sample].notna()]
    
    # Extract "Protein.Group" values, split by ';', and flatten the list
    protein_groups = sample_df['Protein.Group'].dropna().str.split(';')
    unique_proteins = set([protein.strip() for sublist in protein_groups for protein in sublist])
    
    # Count the unique protein groups for the current sample
    unique_protein_counts[sample] = len(unique_proteins)

# Convert the results to a DataFrame for display and saving
unique_protein_df = pd.DataFrame(list(unique_protein_counts.items()), columns=['Sample', 'Unique Protein Count'])

# Display the DataFrame
print(unique_protein_df)

# Save the results to a new Excel file
output_file_path = '/content/unique_protein_counts_per_sample.xlsx'
unique_protein_df.to_excel(output_file_path, index=False)

# Optionally, to download the file in Colab
from google.colab import files
files.download(output_file_path)

