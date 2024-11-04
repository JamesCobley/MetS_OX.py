import gzip
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# File path for the gzipped FASTA file
fasta_file = '/content/uniprotkb_human_AND_model_organism_9606_2024_05_08.fasta (1).gz'

# Function to parse the gzipped FASTA file and extract sequences and UniProt IDs
def parse_fasta_gz(fasta_file):
    sequences = {}
    with gzip.open(fasta_file, 'rt') as file:
        current_id = None
        current_seq = []
        for line in file:
            if line.startswith(">"):
                if current_id:  # If there's a current sequence, process it
                    sequences[current_id] = "".join(current_seq)
                # Get UniProt ID (from the first part of the header line)
                current_id = line.split('|')[1] if '|' in line else line.split()[0][1:]
                current_seq = []
            else:
                current_seq.append(line.strip())
        if current_id:
            sequences[current_id] = "".join(current_seq)
    return sequences

# Parse the FASTA file
proteins = parse_fasta_gz(fasta_file)

# Initialize the amino acid counter and total amino acid count
aa_counter = Counter()
total_aa_count = 0

# Count each amino acid in each protein sequence
for seq in proteins.values():
    aa_counter.update(seq)  # Update counter with amino acids in the sequence
    total_aa_count += len(seq)

# Create a DataFrame for amino acid frequencies
aa_data = []
for aa, count in aa_counter.items():
    percentage = (count / total_aa_count) * 100  # Calculate percentage use
    aa_data.append([aa, count, percentage])

df_aa = pd.DataFrame(aa_data, columns=['Amino Acid', 'Residue Count', 'Percentage Use'])

# Save the DataFrame to an Excel file
output_file_path = '/content/aa_frequency_analysis.xlsx'
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    df_aa.to_excel(writer, sheet_name='Amino Acid Frequency', index=False)

# Optional: Plot a bar chart of amino acid usage percentage
plt.figure(figsize=(10, 6), dpi=300)
plt.bar(df_aa['Amino Acid'], df_aa['Percentage Use'], edgecolor='black')
plt.title('Percentage Usage of Amino Acids')
plt.xlabel('Amino Acid')
plt.ylabel('Percentage Use (%)')
plt.grid(True)
plt.savefig('/content/aa_usage_percentage.png')  # Save plot image
plt.show()

# Output summary statistics
print(f"Total number of amino acid residues: {total_aa_count}")
print(df_aa)

# Download the Excel and plot files (optional if in Google Colab)
from google.colab import files
files.download(output_file_path)
files.download('/content/aa_usage_percentage.png')
