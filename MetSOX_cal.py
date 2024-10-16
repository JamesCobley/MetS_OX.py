import sys
import pandas as pd
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QFileDialog, QCheckBox, QGridLayout, QMessageBox

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label to display instructions or file path
        self.label = QLabel("Upload a DIA-NN Peptide Matrix (Excel file)", self)
        layout.addWidget(self.label)

        # Upload button to select the file
        upload_button = QPushButton("Choose File", self)
        upload_button.clicked.connect(self.show_file_dialog)
        layout.addWidget(upload_button)

        # Confirm button to proceed after file selection
        self.confirm_button = QPushButton("Confirm File Selection", self)
        self.confirm_button.setVisible(False)  # Hidden by default
        self.confirm_button.clicked.connect(self.confirm_file_selection)
        layout.addWidget(self.confirm_button)

        # Layout for sample selection
        self.sample_layout = QGridLayout()
        layout.addLayout(self.sample_layout)

        # Output destination selection
        output_button = QPushButton("Choose Output Folder", self)
        output_button.clicked.connect(self.select_output_folder)
        layout.addWidget(output_button)

        # Execute button to run the analysis
        self.execute_button = QPushButton("Execute Protein Group Counting", self)
        self.execute_button.setVisible(False)  # Hidden by default
        self.execute_button.clicked.connect(self.execute_analysis)
        layout.addWidget(self.execute_button)

        self.setLayout(layout)
        self.setWindowTitle("DIA-NN Protein Group Counter")
        self.setGeometry(300, 300, 600, 400)

    def show_file_dialog(self):
        # Open file dialog to choose Excel file
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open DIA-NN Peptide Matrix", "", "Excel Files (*.xlsx)")
        
        if file_path:
            # Update the label with selected file path
            self.label.setText(f"Selected file: {file_path}")
            self.selected_file = file_path
            # Show the confirm button
            self.confirm_button.setVisible(True)

    def confirm_file_selection(self):
        # Load the Excel file using Pandas
        try:
            self.df = pd.read_excel(self.selected_file)

            # Show sample columns for selection
            self.sample_columns = self.df.columns[9:]  # Assuming sample columns start after the 9th column
            self.checkboxes = []
            for i, col in enumerate(self.sample_columns):
                checkbox = QCheckBox(col)
                self.sample_layout.addWidget(checkbox, i // 2, i % 2)
                self.checkboxes.append(checkbox)

            # Show the execute button after file is loaded
            self.execute_button.setVisible(True)
        except Exception as e:
            # In case of an error, show a message
            QMessageBox.critical(self, "Error", f"Error loading file: {e}")

    def select_output_folder(self):
        folder_dialog = QFileDialog()
        self.output_folder = folder_dialog.getExistingDirectory(self, "Select Output Folder")
        if self.output_folder:
            print(f"Selected output folder: {self.output_folder}")

    def execute_analysis(self):
        try:
            selected_samples = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
            if not selected_samples:
                QMessageBox.warning(self, "No Samples Selected", "Please select at least one sample column.")
                return

            # Dictionary to store unique protein groups for each sample and overlap analysis
            results = {}
            exclusive_counts = {}

            # To keep track of which proteins are detected in how many samples
            protein_detection_counts = pd.DataFrame(0, index=self.df['Protein.Group'], columns=selected_samples)

            for sample in selected_samples:
                # Get rows where the sample column has non-null values
                sample_data = self.df[sample].notna()
                
                # Use a set to track unique protein groups
                unique_protein_groups = set()

                for protein_group in self.df.loc[sample_data, 'Protein.Group']:
                    # Parse UniProt IDs from Protein.Group (split by semicolon if multiple)
                    uniprot_ids = protein_group.split(';')
                    unique_protein_groups.update(uniprot_ids)

                # Mark detected proteins for this sample (only unique proteins)
                for protein_group in unique_protein_groups:
                    protein_detection_counts.loc[protein_group, sample] = 1

                # Only count unique proteins for this sample
                results[sample] = len(unique_protein_groups)

            # Calculate exclusive proteins for each sample (only detected in this sample)
            for sample in selected_samples:
                exclusive_proteins = protein_detection_counts[protein_detection_counts.sum(axis=1) == 1][sample].sum()
                exclusive_counts[sample] = exclusive_proteins

            # Save results to Excel
            output_df = pd.DataFrame({
                "Sample": results.keys(),
                "Protein.Groups": results.values(),
                "Exclusive.Protein.Groups": exclusive_counts.values()
            })

            output_file_path = f"{self.output_folder}/Detected_protein_groups_with_exclusives.xlsx"
            output_df.to_excel(output_file_path, index=False)
            print(f"Results saved to {output_file_path}")

            # Sanity check: Randomly show calculations for one peptide row
            self.sanity_check(selected_samples, protein_detection_counts)

            # Print output complete and close the application
            print("Output complete.")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during analysis: {e}")

    def sanity_check(self, selected_samples, protein_detection_counts):
        # Sanity check to ensure counting is correct
        random_index = random.choice(self.df.index)
        random_row = self.df.iloc[random_index]

        print("\nSanity Check - Random Peptide Row:")
        print(random_row[['Protein.Group', *selected_samples]])

        for sample in selected_samples:
            print(f"\nSanity Check for Sample: {sample}")
            sample_data = self.df[sample].notna()
            unique_proteins = set()

            for protein_group in self.df.loc[sample_data, 'Protein.Group']:
                # Parse UniProt IDs from Protein.Group (split by semicolon if multiple)
                uniprot_ids = protein_group.split(';')
                unique_proteins.update(uniprot_ids)

            print(f"Unique Protein Groups for {sample}: {len(unique_proteins)}")
            print(f"Protein Groups: {unique_proteins}")

        # Check proteins that are exclusive to one sample
        exclusive_proteins = protein_detection_counts[protein_detection_counts.sum(axis=1) == 1]
        print("\nSanity Check - Proteins Detected in Only One Sample:")
        print(exclusive_proteins)

# Main loop
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimpleApp()
    ex.show()
    sys.exit(app.exec_())
