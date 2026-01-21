#!/bin/usr/env python
import os
import pandas as pd

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

# read in the imputed data
imputed_path = os.path.join(script_directory, "Original_Data", "npop5_proteinMatrix_Imputed.BCmTRAQ.txt")
imputed = pd.read_csv(imputed_path, sep="\t").T.reset_index().rename(columns={'index':'sample_id'})



# read in the unimputed data
unimputed_path = os.path.join(script_directory, "Original_Data", "npop5_proteinMatrix_NoImp.BCmTRAQ.txt")
unimputed = pd.read_csv(unimputed_path, sep="\t").T.reset_index().rename(columns={'index':'sample_id'})



# read in the meta data
meta_path = os.path.join(script_directory, "Original_Data", "Protein_cellTypeLabels_postAlignment.txt")
meta_raw = pd.read_csv(meta_path, sep="\t")
meta = meta_raw[meta_raw['id'].str.startswith("Five_")]
meta['id'] = meta['id'].str.removeprefix("Five_")
meta = meta[['id', 'cellType']].rename(columns={'id':'sample_id', 
                                                'cellType':'classification_label'})

labels_to_keep = ["SPG", "St"]
meta = meta[meta['classification_label'].isin(labels_to_keep)]



# filter dfs to the samples in the meta df
samples_to_keep = sorted(list(set(meta['sample_id'].tolist()) & set(imputed['sample_id'].tolist()) & set(unimputed['sample_id'].tolist())))

imputed_final = imputed[imputed['sample_id'].isin(samples_to_keep)]
unimputed_final = unimputed[unimputed['sample_id'].isin(samples_to_keep)]
meta_final = meta[meta['sample_id'].isin(samples_to_keep)]

# label_counts = meta_final['classification_label'].value_counts()
# print(label_counts)



# save the new files
output_directory = os.path.join(script_directory, "NIFty_Ready_Data")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)
    
imputed_final.to_csv(os.path.join(output_directory, "quant_imputed.tsv"), sep="\t", index=False)
unimputed_final.to_csv(os.path.join(output_directory, "quant_unimputed.tsv"), sep="\t", index=False)
meta_final.to_csv(os.path.join(output_directory, "meta.tsv"), sep="\t", index=False)

