#!/bin/usr/env python
import os
import sys
import pandas as pd

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

# file paths
tests = 100

final_predictions = None

test_dir = os.path.join(script_directory, "Test_Ai_Multiclass")

for i in range(tests):
    predictions_path = os.path.join(test_dir, f"Test_{i}", "predictions.tsv")

    predictions = pd.read_csv(predictions_path, sep='\t')

    predictions['test'] = f"Test_{i + 1}"

    if final_predictions is None:
        final_predictions = predictions
    else:
        final_predictions = pd.concat([final_predictions, predictions], ignore_index=True)

# print(final_predictions)

final_predictions.drop('Unnamed: 0', inplace=True, axis=1)

output_path = os.path.join(script_directory, "combined_predictions.tsv")
final_predictions.to_csv(output_path, sep='\t', index=False)

