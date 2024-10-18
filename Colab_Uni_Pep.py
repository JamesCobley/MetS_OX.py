import pandas as pd
import pyarrow.parquet as pq

# Step 1: Load the Parquet file
file_path = '/content/report.parquet'  # Replace with the correct file path
df = pq.read_table(file_path).to_pandas()

# Step 2: Define condition columns (replace with actual column names)
c_condition_runs = ['James_HeLaOXC_30SPD_250ng_120924_S15.raw', 'James_HeLaOXC_30SPD_250ng_120924_S3.raw', 'James_HeLaOXC_30SPD_250ng_120924_S9.raw']  # Runs for condition C
e_condition_runs = ['James_HeLaOXE_30SPD_250ng_120924_S10.raw', 'James_HeLaOXE_30SPD_250ng_120924_S4.raw', 'James_HeLaOXE_30SPD_250ng_120924_S16.raw']  # Runs for condition E

# Step 3: Count unique peptides per run
unique_peptides_per_run = df.groupby('Run')['Stripped.Sequence'].nunique().reset_index()
unique_peptides_per_run.columns = ['Run', 'Unique_Peptide_Count']

# Step 4: Filter the dataframe based on the runs for each condition
df_c = df[df['Run'].isin(c_condition_runs)]
df_e = df[df['Run'].isin(e_condition_runs)]

# Step 5: Count the number of unique peptides detected in each condition
unique_peptides_c = df_c['Stripped.Sequence'].nunique()
unique_peptides_e = df_e['Stripped.Sequence'].nunique()

# Step 6: Print the results
print("Unique peptides detected per run:")
print(unique_peptides_per_run)

print(f"\nTotal number of unique peptides detected in condition C: {unique_peptides_c}")
print(f"Total number of unique peptides detected in condition E: {unique_peptides_e}")
