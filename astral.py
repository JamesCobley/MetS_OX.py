import pandas as pd

# Load the Excel file
file_path = '/content/Astral_Exp_James_1.xlsx'
df = pd.read_excel(file_path)

# Extract the "Protein.Group" column, drop NaN values, and split IDs separated by a semicolon
protein_groups = df['Protein.Group'].dropna().str.split(';')

# Flatten the list of IDs and keep only unique values
unique_proteins = set([protein.strip() for sublist in protein_groups for protein in sublist])

# Count the number of unique protein groups detected
unique_protein_count = len(unique_proteins)

# Display results
print(f"Total unique protein groups detected: {unique_protein_count}")

# Optional: Display the list of unique proteins (can be saved to a file if needed)
print("List of unique protein IDs:")
print(unique_proteins)

# If you want to save the list of unique proteins to a new Excel file
output_file_path = '/content/unique_protein_groups.xlsx'
unique_proteins_df = pd.DataFrame(unique_proteins, columns=['Unique Protein IDs'])
unique_proteins_df.to_excel(output_file_path, index=False)

# Optionally, to download the file in Colab
from google.colab import files
files.download(output_file_path)
