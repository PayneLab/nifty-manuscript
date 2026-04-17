#!/bin/usr/env python

import pandas as pd
import numpy as np
import os
from sklearn.impute import KNNImputer

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)



def filter_proteins_by_class(quant_df, class_labels, fraction_na, proteins_to_keep=[]):
        ''' Filter out proteins that have more than fraction_na of their values as NaN in both classes.'''
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



# read in the meta data
meta_path = os.path.join(script_directory, "Original_Data", "msstats_norm_clustered.csv")
meta = pd.read_csv(meta_path)
# print(len(unimputed['Run'].unique()))
meta = meta.dropna(subset=['cluster'])

meta = meta[['Run', 'cluster']].drop_duplicates().reset_index(drop=True).rename(columns={'Run': 'sample_id', 'cluster': 'classification_label'})
# print(meta)

meta_wt = meta[meta['sample_id'].str.contains('WT')].copy()
meta_mfn = meta[~meta['sample_id'].str.contains('WT')].copy()

meta_smc = meta[meta['classification_label'] == "smc"].copy()
meta_fibro = meta[meta['classification_label'] == "fibro"].copy()
mask_smc = meta_smc['sample_id'].str.contains('WT')
mask_fibro = meta_fibro['sample_id'].str.contains('WT')
meta_smc.loc[mask_smc, 'classification_label'] = 'WT'
meta_smc['classification_label'] = meta_smc['classification_label'].replace('smc', 'MFN')
meta_fibro.loc[mask_fibro, 'classification_label'] = 'WT'
meta_fibro['classification_label'] = meta_fibro['classification_label'].replace('fibro', 'MFN')

if not set(meta_wt['sample_id'].tolist()).isdisjoint(set(meta_mfn['sample_id'].tolist())):
    print("Problem: smaple_id overlaps in WT and MFN groups.")
    sys.exit()

if not set(meta_smc['sample_id'].tolist()).isdisjoint(set(meta_fibro['sample_id'].tolist())):
    print("Problem: smaple_id overlaps in smc and fibro groups.")
    sys.exit()
# print(meta_smc)
# print(meta_fibro)

# label_counts_wt = meta_wt['classification_label'].value_counts()
# print(label_counts_wt)

# label_counts_mfn = meta_mfn['classification_label'].value_counts()
# print(label_counts_mfn)

# label_counts_smc = meta_smc['classification_label'].value_counts()
# print(label_counts_smc)

# label_counts_fibro = meta_fibro['classification_label'].value_counts()
# print(label_counts_fibro)



# read in the unimputed data
marker_proteins = ['SMTN_MOUSE', 'CNN1_MOUSE', 'DPEP1_MOUSE', 'CYGB_MOUSE']
marker_pattern = "|".join(marker_proteins)
unimputed_path = os.path.join(script_directory, "Original_Data", "msstats_norm_summarized.csv")
unimputed = pd.read_csv(unimputed_path)
unimputed = unimputed[['originalRUN', 'Protein', 'LogIntensities']].rename(columns={'originalRUN': 'sample_id'}).drop_duplicates().pivot(index='sample_id', columns='Protein', values='LogIntensities')
# print(unimputed)
unimputed.drop(list(unimputed.filter(regex=marker_pattern, axis=1)), axis=1, inplace=True)
# print(unimputed)
unimputed.reset_index(names='sample_id', inplace=True)
unimputed = unimputed[unimputed['sample_id'].isin(meta['sample_id'])].reset_index(drop=True)



# filter out proteins that are more than 70% missing in every class
unimputed = filter_proteins_by_class(unimputed, meta, 0.7)
unimputed_wt = unimputed[unimputed['sample_id'].isin(meta_wt['sample_id'])].reset_index(drop=True)
unimputed_mfn = unimputed[unimputed['sample_id'].isin(meta_mfn['sample_id'])].reset_index(drop=True)
# print(unimputed_wt)
# print(unimputed_mfn)

unimputed_smc = unimputed[unimputed['sample_id'].isin(meta_smc['sample_id'])].reset_index(drop=True)
unimputed_fibro = unimputed[unimputed['sample_id'].isin(meta_fibro['sample_id'])].reset_index(drop=True)
# print(unimputed_smc)
# print(unimputed_fibro)
unimputed.set_index('sample_id', inplace=True)



# impute missing values
n_neighbors = 3
imputer = KNNImputer(n_neighbors=n_neighbors, weights='distance')

imputed = pd.DataFrame(imputer.fit_transform(unimputed), columns=unimputed.columns)
imputed.index = unimputed.index
unimputed.reset_index(names='sample_id', inplace=True)
imputed.reset_index(names='sample_id', inplace=True)
# print(unimputed)
# print(imputed)


imputed_wt = imputed[imputed['sample_id'].isin(meta_wt['sample_id'])].reset_index(drop=True)
imputed_mfn = imputed[imputed['sample_id'].isin(meta_mfn['sample_id'])].reset_index(drop=True)
# print(unimputed_wt)
# print(imputed_wt)
# print(unimputed_mfn)
# print(imputed_mfn)

imputed_smc = imputed[imputed['sample_id'].isin(meta_smc['sample_id'])].reset_index(drop=True)
imputed_fibro = imputed[imputed['sample_id'].isin(meta_fibro['sample_id'])].reset_index(drop=True)
# print(unimputed_smc)
# print(imputed_smc)
# print(unimputed_fibro)
# print(imputed_fibro)



# write files to the output
output_directory = os.path.join(script_directory, "NIFty_Ready_Data")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

imputed_wt.to_csv(os.path.join(output_directory, "quant_imputed_wt.tsv"), sep="\t", index=False)
unimputed_wt.to_csv(os.path.join(output_directory, "quant_unimputed_wt.tsv"), sep="\t", index=False)
meta_wt.to_csv(os.path.join(output_directory, "meta_wt.tsv"), sep="\t", index=False)

imputed_mfn.to_csv(os.path.join(output_directory, "quant_imputed_mfn.tsv"), sep="\t", index=False)
unimputed_mfn.to_csv(os.path.join(output_directory, "quant_unimputed_mfn.tsv"), sep="\t", index=False)
meta_mfn.to_csv(os.path.join(output_directory, "meta_mfn.tsv"), sep="\t", index=False)

imputed_smc.to_csv(os.path.join(output_directory, "quant_imputed_smc.tsv"), sep="\t", index=False)
unimputed_smc.to_csv(os.path.join(output_directory, "quant_unimputed_smc.tsv"), sep="\t", index=False)
meta_smc.to_csv(os.path.join(output_directory, "meta_smc.tsv"), sep="\t", index=False)

imputed_fibro.to_csv(os.path.join(output_directory, "quant_imputed_fibro.tsv"), sep="\t", index=False)
unimputed_fibro.to_csv(os.path.join(output_directory, "quant_unimputed_fibro.tsv"), sep="\t", index=False)
meta_fibro.to_csv(os.path.join(output_directory, "meta_fibro.tsv"), sep="\t", index=False)

