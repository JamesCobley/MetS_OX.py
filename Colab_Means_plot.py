import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ttest_ind
import numpy as np

# Define your data
data = {'Sample': ['C1', 'C2', 'C3', 'E1', 'E2', 'E3'],
        'Unique Protein Groups': [6608, 6173, 6332, 6154, 6238, 6325]}

# Create a DataFrame
df = pd.DataFrame(data)

# Separate the 'C' group and 'E' group
c_group = df[df['Sample'].str.contains('C')]['Unique Protein Groups']
e_group = df[df['Sample'].str.contains('E')]['Unique Protein Groups']

# Calculate the means and standard deviations for each group
c_mean = c_group.mean()
e_mean = e_group.mean()
c_sd = c_group.std()
e_sd = e_group.std()

# Print the means and SDs
print(f'C group mean: {c_mean:.2f}, SD: {c_sd:.2f}')
print(f'E group mean: {e_mean:.2f}, SD: {e_sd:.2f}')

# Perform an unpaired t-test between C and E groups
t_stat, p_value = ttest_ind(c_group, e_group)

# Create the plot
plt.figure(figsize=(8, 6), dpi=300)

# Plot the means with error bars for SD (remove bar outline by not setting edgecolor)
plt.bar(['C', 'E'], [c_mean, e_mean], yerr=[c_sd, e_sd], color=['#1f77b4', '#2ca02c'], capsize=10, alpha=0.6, label='Mean ± SD')

# Plot individual data points
plt.scatter(['C'] * len(c_group), c_group, color='black', s=100, edgecolor='black', zorder=2, label='C Group Values')
plt.scatter(['E'] * len(e_group), e_group, color='grey', s=100, edgecolor='black', zorder=2, label='E Group Values')

# Add title and labels

plt.xlabel('Group', fontsize=12)
plt.ylabel('Protein Groups', fontsize=12)

# Set y-axis limit to slightly above the maximum value in the dataset for better scaling
plt.ylim(6000, max(df['Unique Protein Groups']) + 500)

# Annotate the plot with the t-test result (p-value)
plt.text(0.5, max(df['Unique Protein Groups']) + 100, f'p-value: {p_value:.4f}', ha='center', fontsize=12)

# Add legend
plt.legend()

# Save the plot as a PNG image with 300 DPI
plt.savefig('/content/unique_protein_groups_plot_adjusted.png', dpi=300)

# Show the plot
plt.show()

# Print the t-test result for verification
print(f'T-test result: t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}')
