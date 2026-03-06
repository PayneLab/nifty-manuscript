#!/bin/usr/env python

import pandas as pd
import numpy as np
import pyarrow
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



# read in the unimputed data and format for NIFty
unimputed_path = os.path.join(script_directory, "Original_Data", "report.parquet")
unimputed = pd.read_parquet(unimputed_path)
unimputed = unimputed[~unimputed['Run'].str.contains("_human_CD34_")]  # not enough cells of CD34, remove them
unimputed = unimputed[unimputed['Global.PG.Q.Value'] < 0.01]
unimputed = unimputed[~unimputed['Protein.Group'].str.contains("contam")]
unimputed = unimputed[['Run', 'Protein.Group', 'PG.MaxLFQ']].drop_duplicates().pivot(index='Run', columns='Protein.Group', values='PG.MaxLFQ')
unimputed.drop(columns=[''], inplace=True)
unimputed.reset_index(names='sample_id', inplace=True)
# print(unimputed)

meta = unimputed[['sample_id']].copy()
meta['classification_label'] = unimputed['sample_id'].str.extract(r'_(u937)_WT_|_human_(CD34)_|_sc(HEK)_').bfill(axis=1).iloc[:, 0]
# print(meta)

label_counts = meta['classification_label'].value_counts()
# print(label_counts)



# filter out proteins that are more than 70% missing in every class
unimputed = filter_proteins_by_class(unimputed, meta, 0.7)
unimputed.set_index('sample_id', inplace=True)
# print(unimputed)



# impute missing values
n_neighbors = 3
imputer = KNNImputer(n_neighbors=n_neighbors, weights='distance')

imputed = pd.DataFrame(imputer.fit_transform(unimputed), columns=unimputed.columns)
imputed.index = unimputed.index
unimputed.reset_index(names='sample_id', inplace=True)
imputed.reset_index(names='sample_id', inplace=True)
# print(unimputed)
# print(imputed)



# write files to the output
output_directory = os.path.join(script_directory, "NIFty_Ready_Data")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

imputed.to_csv(os.path.join(output_directory, "quant_imputed.tsv"), sep="\t", index=False)
unimputed.to_csv(os.path.join(output_directory, "quant_unimputed.tsv"), sep="\t", index=False)
meta.to_csv(os.path.join(output_directory, "meta.tsv"), sep="\t", index=False)

