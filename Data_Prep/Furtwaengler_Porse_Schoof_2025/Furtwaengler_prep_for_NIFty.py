#!/bin/usr/env python

import anndata
import pandas as pd
import numpy as np
import os

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

file_path = os.path.join(script_directory, "Original_Data", "hBM_glue_celltype.h5ad")
data = anndata.read_h5ad(file_path)



# extract the meta data
meta_data = data.obs
meta_data.index.name = "sample_id"
meta_data.reset_index(inplace=True)
meta_data = meta_data[['sample_id', 'cell_type']].rename(columns={'cell_type': 'classification_label'})

labels_to_keep = ['HSC', 'EMP', 'Early Eryth']
meta_data = meta_data[meta_data['classification_label'].isin(labels_to_keep)]



# Extract the quant data
quant_data_var_names = data.var_names
quant_data_obs_names = data.obs_names

quant_data_imputed = pd.DataFrame(data.layers["batchcorr_norm_log2_imputed"], columns=quant_data_var_names)
quant_data_imputed['sample_id'] = meta_data['sample_id']

quant_data_unimputed = pd.DataFrame(data.layers["batchcorr_norm_log2"], columns=quant_data_var_names)
quant_data_unimputed['sample_id'] = meta_data['sample_id']
mask_diff = (quant_data_imputed != quant_data_unimputed)
quant_data_unimputed[mask_diff] = np.nan



# filter dfs to the samples in the meta df
samples_to_keep = sorted(list(set(meta_data['sample_id'].tolist()) & set(quant_data_imputed['sample_id'].tolist()) & set(quant_data_unimputed['sample_id'].tolist())))

imputed_final = quant_data_imputed[quant_data_imputed['sample_id'].isin(samples_to_keep)]
unimputed_final = quant_data_unimputed[quant_data_unimputed['sample_id'].isin(samples_to_keep)]
meta_final = meta_data[meta_data['sample_id'].isin(samples_to_keep)]

# label_counts = meta_final['classification_label'].value_counts()
# print(label_counts)



# save the new files
output_directory = os.path.join(script_directory, "NIFty_Ready_Data")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

imputed_final.to_csv(os.path.join(output_directory, "quant_imputed.tsv"), sep="\t", index=False)
unimputed_final.to_csv(os.path.join(output_directory, "quant_unimputed.tsv"), sep="\t", index=False)
meta_final.to_csv(os.path.join(output_directory, "meta.tsv"), sep="\t", index=False)





