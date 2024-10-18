import pandas as pd
import pyarrow.parquet as pq

# Replace 'your_file.parquet' with the actual file path if needed
file_path = '/content/report.parquet'

# Load the PyArrow (parquet) file into a Pandas DataFrame
df = pq.read_table(file_path).to_pandas()

# Step 1: Create a flag for UniMod:35 presence in the 'Modified.Sequence'
df['Contains_UniMod35'] = df['Modified.Sequence'].str.contains('UniMod:35')

# Step 2: Separate experimental (OXE) and control (OXC) runs
experimental_runs = df[df['Run'].str.contains('OXE')]
control_runs = df[df['Run'].str.contains('OXC')]

# Step 3: Identify shared peptides between experimental and control runs (using 'Stripped.Sequence')
shared_peptides = pd.merge(
    experimental_runs[['Stripped.Sequence', 'Run']],
    control_runs[['Stripped.Sequence', 'Run']],
    on='Stripped.Sequence',
    how='inner'
)['Stripped.Sequence'].unique()

# Filter the dataframe to keep only shared peptides
df_shared = df[df['Stripped.Sequence'].isin(shared_peptides)]

# Step 4: Group by peptide sequence and oxidation status, then calculate impact metrics
impact_analysis = df_shared.groupby(['Stripped.Sequence', 'Contains_UniMod35']).agg({
    'RT': 'mean',  # Average retention time
    'Precursor.Quantity': 'mean',  # Average signal intensity
    'Q.Value': 'mean'  # Average confidence score
}).reset_index()

# Step 5: Split the data into oxidized (UniMod:35) and non-oxidized versions for comparison
oxidized = impact_analysis[impact_analysis['Contains_UniMod35'] == True]
non_oxidized = impact_analysis[impact_analysis['Contains_UniMod35'] == False]

# Step 6: Merge the oxidized and non-oxidized data to compare
comparison = pd.merge(
    non_oxidized,
    oxidized,
    on='Stripped.Sequence',
    suffixes=('_Non_Oxidized', '_Oxidized')
)

# Step 7: Calculate the impact of oxidation on RT, intensity, and confidence
comparison['RT_Impact'] = comparison['RT_Oxidized'] - comparison['RT_Non_Oxidized']
comparison['Intensity_Impact'] = comparison['Precursor.Quantity_Oxidized'] - comparison['Precursor.Quantity_Non_Oxidized']
comparison['Confidence_Impact'] = comparison['Q.Value_Oxidized'] - comparison['Q.Value_Non_Oxidized']

# Step 8: Print the results
print("Impact of Methionine Oxidation (UniMod:35) on Shared Peptides:")
print(comparison[['Stripped.Sequence', 'RT_Impact', 'Intensity_Impact', 'Confidence_Impact']].to_string(index=False))

# Step 9: Optionally, save the results to an Excel file for further review
output_file = '/content/Methionine_Oxidation_Impact_Analysis.xlsx'
comparison.to_excel(output_file, index=False)

# Download the resultant Excel file (for Google Colab)
from google.colab import files
files.download(output_file)
