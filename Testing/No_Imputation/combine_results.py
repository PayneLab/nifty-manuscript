#!/bin/usr/env python
import os
import sys
import pandas as pd

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

# file paths
output_paths = [os.path.join(script_directory, "Test_Ai_Imputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Ai_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Furtwaengler_Imputed_HSCxEarlyEryth", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Furtwaengler_Unimputed_HSCxEarlyEryth", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Furtwaengler_Imputed_HSCxEMP", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Furtwaengler_Unimputed_HSCxEMP", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Khan_Imputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Khan_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Leduc_Imputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Leduc_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Montalvo_Imputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Montalvo_Unimputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Petrosius_Imputed", "NIFty_Output"), 
                os.path.join(script_directory, "Test_Petrosius_Unimputed", "NIFty_Output")]


dataset = []
data_missingness = []
cell_types = []
num_samples_per_class = []
test_num = []
val_accuracy = []
val_precision = []
val_recall = []

# loop through directories in each of the above locations and read the "model_information.txt" file
for output_path in output_paths:
    print(f"Currently analyzing: {output_path}")

    for dirpath, dirnames, filenames in os.walk(output_path):
        for subdir in dirnames:
            print(f"\t- {subdir}")
            
            model_info_path = os.path.join(dirpath, subdir, "model_information.txt")

            test_info = subdir.split("_")
            dataset.append(test_info[0])
            data_missingness.append(test_info[1])
            if test_info[0] == "Furtwaengler":
                cell_types.append(test_info[2])
                num_samples_per_class.append(int(test_info[3].replace("Split", "")))
                test_num.append(int(test_info[4].replace("Test", "")))
            else:
                cell_types.append(None)
                num_samples_per_class.append(int(test_info[2].replace("Split", "")))
                test_num.append(int(test_info[3].replace("Test", "")))

            with open(model_info_path) as in_file:
                for line in in_file:
                    if line.startswith("Accuracy:") or line.startswith("Precision:") or line.startswith("Recall:"):
                        line = line.strip().split(": ")

                        if line[0] == "Accuracy":
                            val_accuracy.append(float(line[1]))
                        elif line[0] == "Precision":
                            val_precision.append(float(line[1]))
                        elif line[0] == "Recall":
                            val_recall.append(float(line[1]))

        break

final_output_path = os.path.join(script_directory, "combined_results.tsv")
print(f"Saving final output to: {final_output_path}")
final_output = pd.DataFrame({
    'Dataset': dataset, 
    'Data Type': data_missingness, 
    'Cell Types': cell_types, 
    'Samples per Class': num_samples_per_class, 
    'Test': test_num, 
    'Validation Accuracy': val_accuracy, 
    'Validation Precision': val_precision, 
    'Validation Recall': val_recall
})

final_output.to_csv(final_output_path, sep='\t', index=False)
