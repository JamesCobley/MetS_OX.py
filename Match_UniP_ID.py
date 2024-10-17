import pandas as pd

# Load the human proteome methionine analysis file (with methionine counts)
methionine_file = '/content/human_proteome_methionine_analysis.xlsx'
df_methionine = pd.read_excel(methionine_file)

# Load the Sig_diff file (with LFQ values and UniProt IDs)
sig_diff_file = '/content/Sig_diff.xlsx'
df_sig_diff = pd.read_excel(sig_diff_file)

# Ensure that both dataframes use the same column name for protein IDs (standardize)
# In df_methionine, the ID column is 'UniProt ID', in df_sig_diff it is 'Protein.Group'
df_methionine.rename(columns={'UniProt ID': 'Protein.Group'}, inplace=True)

# Create a dictionary for quick lookup of M values by Protein.Group (UniProt ID)
methionine_dict = dict(zip(df_methionine['Protein.Group'], df_methionine['M']))

# Function to find the first matching UniProt ID from the Protein.Group column in Sig_diff
def find_first_matching_m(protein_group):
    # Split the Protein.Group by semicolon to handle multiple UniProt IDs
    protein_ids = protein_group.split(';')
    
    # Iterate through each UniProt ID and strip off any isoform part (e.g., "-2")
    for pid in protein_ids:
        base_id = pid.split('-')[0]  # Keep only the base ID (ignore the isoform part)
        if base_id in methionine_dict:
            return methionine_dict[base_id]  # Return the M count for the first matching base UniProt ID
    
    return None  # Return None if no match is found

# Apply the function to the 'Protein.Group' column in Sig_diff to find the matching M value
df_sig_diff['M'] = df_sig_diff['Protein.Group'].apply(find_first_matching_m)

# Write the merged dataframe with the new 'M' column to a new Excel file
output_file = '/content/Sig_diff_M.xlsx'
df_sig_diff.to_excel(output_file, index=False)

# Print success message and show the first few rows of the new dataframe
print(f"Data merged successfully! New file saved as: {output_file}")
df_sig_diff.head()

# Download the resultant file if needed (for Google Colab)
from google.colab import files
files.download(output_file)
