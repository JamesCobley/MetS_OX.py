import pandas as pd

# Assuming your dataframe is already loaded from the PyArrow file
# df = (code to load your dataframe from PyArrow)

# Step 1: Define functions to count methionine (M) and cysteine (C) residues in the 'Stripped.Sequence'
def count_methionine(sequence):
    return sequence.count('M')  # Count occurrences of 'M'

def count_cysteine(sequence):
    return sequence.count('C')  # Count occurrences of 'C'

# Step 2: Apply the methionine and cysteine count functions to the 'Stripped.Sequence'
df['Methionine_Count'] = df['Stripped.Sequence'].apply(count_methionine)
df['Cysteine_Count'] = df['Stripped.Sequence'].apply(count_cysteine)

# Step 3: Drop duplicate peptides per run (keep the first occurrence)
df_unique = df.drop_duplicates(subset=['Run', 'Stripped.Sequence'])

# Step 4: Group by 'Run' and sum the methionine and cysteine counts for each run
total_counts_per_run = df_unique.groupby('Run')[['Methionine_Count', 'Cysteine_Count']].sum().reset_index()

# Step 5: Print the total Methionine and Cysteine count per run
print("Total Methionine and Cysteine Residues Detected Per Run:")
print(total_counts_per_run.to_string(index=False))

# Step 6: Optionally, return the total dataframe for further use if needed
total_counts_per_run.head()  # Display first few rows of the total counts per run
