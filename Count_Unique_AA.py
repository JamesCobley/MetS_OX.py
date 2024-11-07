import pandas as pd
import pyarrow.parquet as pq

# Load the Parquet file
file_path = '/content/report (1).parquet'  # Replace with the correct file path
df = pq.read_table(file_path).to_pandas()

# Define the amino acids and condition runs
amino_acids = "ACDEFGHIKLMNPQRSTVWY"  # All 20 standard amino acids
c_condition_runs = ['James_HeLaOXC_30SPD_250ng_120924_S15.raw', 'James_HeLaOXC_30SPD_250ng_120924_S3.raw', 'James_HeLaOXC_30SPD_250ng_120924_S9.raw']
e_condition_runs = ['James_HeLaOXE_30SPD_250ng_120924_S10.raw', 'James_HeLaOXE_30SPD_250ng_120924_S4.raw', 'James_HeLaOXE_30SPD_250ng_120924_S16.raw']

# Step 1: Function to count each amino acid in a sequence
def count_amino_acids(sequence):
    return {aa: sequence.count(aa) for aa in amino_acids}

# Step 2: Apply the function to the 'Stripped.Sequence' column and expand into separate columns
aa_counts_df = df['Stripped.Sequence'].apply(count_amino_acids).apply(pd.Series)
df = pd.concat([df, aa_counts_df], axis=1)

# Step 3: Drop duplicate peptides per run (keep the first occurrence)
df_unique = df.drop_duplicates(subset=['Run', 'Stripped.Sequence'])

# Step 4: Group by 'Run' and sum the amino acid counts for each run
total_counts_per_run = df_unique.groupby('Run')[list(amino_acids)].sum().reset_index()

# Step 5: Export the total counts to an Excel file
output_path = '/content/amino_acid_counts_per_run.xlsx'  # Replace with your desired file path
total_counts_per_run.to_excel(output_path, index=False)

print("Results exported to:", output_path)
