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
rules = []
missingness_class_a = []
missingness_class_b = []

for output_path in test_paths:
    print(f"Currently analyzing: {output_path}")

    for dirpath, dirnames, filenames in os.walk(output_path):
        for subdir in dirnames:
            if "Split50" not in subdir and "Split100" not in subdir:
                continue
            print(f"\t- {subdir}")
            
            features_path = os.path.join(dirpath, subdir, "selected_features.tsv")
            fs_quant_path = os.path.join(output_path, "FS_Datasets", f"{subdir}_FS_Quant.tsv")
            fs_meta_path = os.path.join(output_path, "FS_Datasets", f"{subdir}_FS_Meta.tsv")

            test_info = subdir.split("_")

            features = pd.read_csv(features_path, sep='\t')
            fs_quant = pd.read_csv(fs_quant_path, sep='\t')
            fs_meta = pd.read_csv(fs_meta_path, sep='\t')

            prot_1 = features['Protein1'].tolist()
            prot_2 = features['Protein2'].tolist()

            class_a = fs_meta["classification_label"].tolist()[0]

            samples_class_a = fs_meta[fs_meta['classification_label'] == class_a]['sample_id'].tolist()
            samples_class_b = fs_meta[fs_meta['classification_label'] != class_a]['sample_id'].tolist()

            num_samples_class_a = len(samples_class_a)
            num_samples_class_b = len(samples_class_b)

            for prot1, prot2 in zip(prot_1, prot_2):
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


                rule = f"{prot1}|{prot2}"
                rules.append(rule)

                missingness_a = fs_quant.loc[fs_quant["sample_id"].isin(samples_class_a),prot1].isna().sum() / num_samples_class_a
                missingness_b = fs_quant.loc[fs_quant["sample_id"].isin(samples_class_b),prot1].isna().sum() / num_samples_class_b

                missingness_class_a.append(missingness_a)
                missingness_class_b.append(missingness_b)


final_output_path = os.path.join(script_directory, "class-correlated_missingness_analysis_results.tsv")
print(f"Saving final output to: {final_output_path}")
final_output = pd.DataFrame({
    'Dataset': dataset, 
    'Data Type': data_missingness, 
    'Cell Types': cell_types, 
    'Samples per Class': num_samples_per_class, 
    'Test': test_num, 
    'Rule': rules,
    'Missingness Class A': missingness_class_a, 
    'Missingness Class B': missingness_class_b
})

final_output.to_csv(final_output_path, sep='\t', index=False)






