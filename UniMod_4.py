import pandas as pd

# Assuming your dataframe is already loaded from the PyArrow file
# df = (code to load your dataframe from PyArrow)

# Step 1: Define a function to count the occurrences of "UniMod:4" in the 'Modified.Sequence'
def count_unimod_4(sequence):
    return sequence.count('UniMod:4')  # Count occurrences of 'UniMod:4'

# Step 2: Apply the function to the 'Modified.Sequence' column
df['UniMod_4_Count'] = df['Modified.Sequence'].apply(count_unimod_4)

# Step 3: Drop duplicate peptides per run (keep the first occurrence)
df_unique = df.drop_duplicates(subset=['Run', 'Modified.Sequence'])

# Step 4: Group by 'Run' and sum the UniMod:4 counts for each run
total_unimod_4_per_run = df_unique.groupby('Run')['UniMod_4_Count'].sum().reset_index()

# Step 5: Print the total UniMod:4 count per run
print("Total UniMod:4 (Carbamidomethylation on Cysteine) Detected Per Run:")
print(total_unimod_4_per_run.to_string(index=False))

# Step 6: Optionally, return the total dataframe for further use if needed
total_unimod_4_per_run.head()  # Display first few rows of the total UniMod:4 count per run
