import gzip
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# File path for the gzipped FASTA file
fasta_file = '/content/uniprotkb_human_AND_model_organism_9606_2024_05_08.fasta (1).gz'

# Initialize counters and lists
total_methionine_count = 0
total_aa_count = 0
proteins_with_m = 0
proteins_data = []

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

# Analyze the proteins and count methionine residues
for uniprot_id, seq in proteins.items():
    m_count = seq.count('M')
    total_methionine_count += m_count
    total_aa_count += len(seq)
    
    # Count the number of proteins with at least one M
    if m_count > 0:
        proteins_with_m += 1
    
    # Store protein data: UniProt ID, Total Amino Acids (TAA), and M count
    proteins_data.append([uniprot_id, len(seq), m_count])

# Calculate the percentage frequency of M residues out of all amino acids
m_percentage = (total_methionine_count / total_aa_count) * 100

# Create a DataFrame with UniProt ID, Total Amino Acids, and Methionine count
df_proteins = pd.DataFrame(proteins_data, columns=['UniProt ID', 'TAA', 'M'])

# Save the DataFrame to an Excel file
output_file_path = '/content/human_proteome_methionine_analysis.xlsx'
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    df_proteins.to_excel(writer, sheet_name='Proteins Methionine Count', index=False)

# Plot histogram: Frequency of proteins by number of M residues
plt.figure(figsize=(10, 6), dpi=300)
plt.hist(df_proteins['M'], bins=range(df_proteins['M'].max() + 1), edgecolor='black')
plt.title('Frequency of Proteins by Number of Methionine Residues')
plt.xlabel('Number of Methionine Residues (M)')
plt.ylabel('Number of Proteins')
plt.grid(True)
plt.savefig('/content/methionine_histogram.png')  # Save histogram image
plt.show()

# Output summary statistics
print(f"Total number of methionine residues (M): {total_methionine_count}")
print(f"Total number of unique proteins: {len(proteins)}")
print(f"Number of proteins with at least one M: {proteins_with_m}")
print(f"Percentage frequency of methionine (M) residues out of total amino acids: {m_percentage:.2f}%")

# Download the Excel and plot files (optional if in Google Colab)
from google.colab import files
files.download(output_file_path)
files.download('/content/methionine_histogram.png')
