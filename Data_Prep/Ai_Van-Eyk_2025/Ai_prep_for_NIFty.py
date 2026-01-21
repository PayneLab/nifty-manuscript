#!/bin/usr/env python

import pandas as pd
import numpy as np
import os
from sklearn.impute import KNNImputer

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)



def filter_proteins_by_class(quant_df, class_labels, fraction_na, proteins_to_keep=[]):
        ''' Filter out proteins that have more than fraction_na of their values as NaN in all classes.'''
        quant_labels_df = quant_df.merge(class_labels, on='sample_id', how='inner')
        # print(quant_labels_df.shape)
        quant_labels_df = quant_labels_df.dropna(subset=[class_labels.columns[0]])
        # print(quant_labels_df.shape)

        label_col = 'classification_label'

        classes = class_labels['classification_label'].unique()

        proteins_to_drop = []

        for col in quant_df.columns:
            drop = True

            if col in proteins_to_keep:
                drop = False
            else:
                for cls in classes:
                    class_subset = quant_labels_df[quant_labels_df[label_col] == cls]

                    nan_ratio = class_subset[col].isna().mean()

                    if nan_ratio <= fraction_na:
                        drop = False
                        break

            if drop:
                proteins_to_drop.append(col)

        filtered_df = quant_df.drop(columns=proteins_to_drop)
        # print(filtered_df)

        # Check if filtered_df is empty
        if filtered_df.shape[1] <= 1:  # only sample_id column left
            return 10

        return filtered_df



# read in the unimputed data - iCMs and format for NIFty
unimputed_path_iPSC = os.path.join(script_directory, "Original_Data", "report1.tsv")
unimputed_iPSC = pd.read_csv(unimputed_path_iPSC, sep="\t")
unimputed_iPSC = unimputed_iPSC[unimputed_iPSC['Run'].str.contains("1cell")]
unimputed_iPSC = unimputed_iPSC[unimputed_iPSC['Lib.PG.Q.Value'] < 0.01]
unimputed_iPSC = unimputed_iPSC[['Run', 'Protein.Group', 'PG.MaxLFQ']].drop_duplicates().pivot(index='Run', columns='Protein.Group', values='PG.MaxLFQ')
unimputed_iPSC.reset_index(names='sample_id', inplace=True)
# print(unimputed_iPSC)

meta_iPSC = unimputed_iPSC[['sample_id']].copy()
meta_iPSC['classification_label'] = unimputed_iPSC['sample_id'].str.extract(r'_(day\d+)_')
# print(meta_iPSC)

label_counts = meta_iPSC['classification_label'].value_counts()
print(label_counts)



# filter out proteins that are more than 70% missing in every class
unimputed_iPSC = filter_proteins_by_class(unimputed_iPSC, meta_iPSC, 0.7)
unimputed_iPSC.set_index('sample_id', inplace=True)
# print(unimputed_iPSC)



# impute missing values
n_neighbors = 3
imputer = KNNImputer(n_neighbors=n_neighbors, weights='distance')

imputed_iPSC = pd.DataFrame(imputer.fit_transform(unimputed_iPSC), columns=unimputed_iPSC.columns)
imputed_iPSC.index = unimputed_iPSC.index
unimputed_iPSC.reset_index(names='sample_id', inplace=True)
imputed_iPSC.reset_index(names='sample_id', inplace=True)
# print(unimputed_iPSC)
# print(imputed_iPSC)



# write files to the output
output_directory = os.path.join(script_directory, "NIFty_Ready_Data")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

imputed_iPSC.to_csv(os.path.join(output_directory, "quant_imputed.tsv"), sep="\t", index=False)
unimputed_iPSC.to_csv(os.path.join(output_directory, "quant_unimputed.tsv"), sep="\t", index=False)
meta_iPSC.to_csv(os.path.join(output_directory, "meta.tsv"), sep="\t", index=False)

