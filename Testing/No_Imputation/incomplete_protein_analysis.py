#!/bin/usr/env python
import os
import sys
import pandas as pd

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

# file paths
output_paths = [os.path.join(script_directory, "Test_Ai_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Furtwaengler_Unimputed_HSCxEarlyEryth", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Furtwaengler_Unimputed_HSCxEMP", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Khan_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Leduc_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Montalvo_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Petrosius_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Saddic_Unimputed_WT", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Saddic_Unimputed_MFN", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Saddic_Unimputed_SMC", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Saddic_Unimputed_Fibro", "NIFty_Output")]


dataset = []
data_missingness = []
cell_types = []
num_samples_per_class = []
test_num = []
num_total_proteins = []
num_complete_proteins = []
num_complete_pairs = []

# loop through directories in each of the above locations and read the "model_information.txt" file
for output_path in test_paths:
    print(f"Currently analyzing: {output_path}")

    for dirpath, dirnames, filenames in os.walk(output_path):
        for subdir in dirnames:
            if "Split50" not in subdir and "Split100" not in subdir:
                continue
            print(f"\t- {subdir}")
            
            features_path = os.path.join(dirpath, subdir, "selected_features.tsv")
            fs_input_path = os.path.join(output_path, "FS_Datasets", f"{subdir}_FS_Quant.tsv")
            train_test_input_path = os.path.join(output_path, "Train_Test_Datasets", f"{subdir}_Train_Test_Quant.tsv")
            validate_input_path = os.path.join(output_path, "Validate_Datasets", f"{subdir}_Validate_Quant.tsv")

            test_info = subdir.split("_")
            dataset.append(test_info[0])
            data_missingness.append(test_info[1])
            if test_info[0] == "Furtwaengler" or test_info[0] == "Saddic":
                cell_types.append(test_info[2])
                num_samples_per_class.append(int(test_info[3].replace("Split", "")))
                test_num.append(int(test_info[4].replace("Test", "")))
            else:
                cell_types.append(None)
                num_samples_per_class.append(int(test_info[2].replace("Split", "")))
                test_num.append(int(test_info[3].replace("Test", "")))

            features = pd.read_csv(features_path, sep='\t')
            fs_quant = pd.read_csv(fs_input_path, sep='\t').drop('sample_id', axis=1)
            total_proteins = len(fs_quant.columns)
            num_total_proteins.append(total_proteins)
            fs_quant = fs_quant.dropna(axis=1)
            train_test_quant = pd.read_csv(train_test_input_path, sep='\t').dropna(axis=1).drop('sample_id', axis=1)
            validate_quant = pd.read_csv(validate_input_path, sep='\t').dropna(axis=1).drop('sample_id', axis=1)

            fs_proteins = set(fs_quant.columns.tolist())
            train_test_proteins = set(train_test_quant.columns.tolist())
            validate_proteins = set(validate_quant.columns.tolist())

            complete_proteins = fs_proteins & train_test_proteins & validate_proteins

            complete_pairs = 0
            protein1 = features['Protein1'].tolist()
            protein2 = features['Protein2'].tolist()

            for prot1, prot2 in zip(protein1, protein2):
                if prot1 in complete_proteins and prot2 in complete_proteins:
                    complete_pairs += 1

            num_complete_proteins.append(len(complete_proteins))
            num_complete_pairs.append(complete_pairs)

            

final_output_path = os.path.join(script_directory, "incomplete_protein_analysis_results.tsv")
print(f"Saving final output to: {final_output_path}")
final_output = pd.DataFrame({
    'Dataset': dataset, 
    'Data Type': data_missingness, 
    'Cell Types': cell_types, 
    'Samples per Class': num_samples_per_class, 
    'Test': test_num, 
    'Number Proteins': num_total_proteins,
    'Number Complete Proteins': num_complete_proteins, 
    'Number Complete Pairs': num_complete_pairs
})

final_output.to_csv(final_output_path, sep='\t', index=False)
