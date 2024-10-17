import pandas as pd
import matplotlib.pyplot as plt

# Data from the M count and UniMod:35 count
data = {
    'Run': [
        'James_HeLaOXC_30SPD_250ng_120924_S15.raw',
        'James_HeLaOXC_30SPD_250ng_120924_S3.raw',
        'James_HeLaOXC_30SPD_250ng_120924_S9.raw',
        'James_HeLaOXE_30SPD_250ng_120924_S10.raw',
        'James_HeLaOXE_30SPD_250ng_120924_S16.raw',
        'James_HeLaOXE_30SPD_250ng_120924_S4.raw'
    ],
    'Methionine_Count': [4015, 4448, 3870, 2835, 2919, 2791],
    'UniMod_35_Count': [444, 499, 340, 2827, 2909, 2791]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Calculate the percentage of oxidized methionine (UniMod:35/Methionine_Count * 100)
df['Oxidation_Percentage'] = (df['UniMod_35_Count'] / df['Methionine_Count']) * 100

# Print the updated DataFrame with oxidation percentage
print(df)

# Plotting the Methionine Count and UniMod:35 Count for comparison
plt.figure(figsize=(10, 6))
plt.bar(df['Run'], df['Methionine_Count'], label='Methionine Count', alpha=0.6)
plt.bar(df['Run'], df['UniMod_35_Count'], label='UniMod:35 Count', alpha=0.6)
plt.xticks(rotation=90)
plt.ylabel('Count')
plt.title('Methionine Count vs UniMod:35 Count per Run')
plt.legend()
plt.tight_layout()
plt.show()

# Plotting the percentage of oxidized methionines per run
plt.figure(figsize=(10, 6))
plt.bar(df['Run'], df['Oxidation_Percentage'], label='Oxidation Percentage', color='orange')
plt.xticks(rotation=90)
plt.ylabel('Oxidation Percentage (%)')
plt.title('Percentage of Methionine Oxidized (UniMod:35) per Run')
plt.tight_layout()
plt.show()
