#!bin/usr/env python
import os
import sys
import random
import math
import subprocess
import pandas as pd
from pathlib import Path

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

# input files
quant_file = os.path.join(script_directory, os.pardir, os.pardir, 'Data_Prep', 'Khan_Elcheikhali_Slavov_2024', 'NIFty_Ready_Data', 'quant_unimputed.tsv')
meta_file = os.path.join(script_directory, os.pardir, os.pardir, 'Data_Prep', 'Khan_Elcheikhali_Slavov_2024', 'NIFty_Ready_Data', 'meta.tsv')

quant_table = pd.read_csv(quant_file, sep='\t')
meta_table = pd.read_csv(meta_file, sep='\t')

SPG_samples = set(meta_table[meta_table['classification_label'] == "SPG"]['sample_id'].tolist())
St_samples = set(meta_table[meta_table['classification_label'] == "St"]['sample_id'].tolist())


# set up testing information
splits = [50, 100]  # num samples per class to start with and be split into train test
tests = 100
fs_ratio = 0.3
train_test_ratio = 0.7
num_samples_per_class_validation = 50


# create the directories for files information
main_output_dir = os.path.join(script_directory, 'Test_Khan_Unimputed')
if not os.path.exists(main_output_dir):
    os.mkdir(main_output_dir)

fs_output_dir = os.path.join(main_output_dir, "FS_Datasets")
if not os.path.exists(fs_output_dir):
    os.mkdir(fs_output_dir)

train_test_output_dir = os.path.join(main_output_dir, "Train_Test_Datasets")
if not os.path.exists(train_test_output_dir):
    os.mkdir(train_test_output_dir)

validate_output_dir = os.path.join(main_output_dir, "Validate_Datasets")
if not os.path.exists(validate_output_dir):
    os.mkdir(validate_output_dir)

config_output_dir = os.path.join(main_output_dir, "Config_Files")
if not os.path.exists(config_output_dir):
    os.mkdir(config_output_dir)

NIFty_output_dir = os.path.join(main_output_dir, "NIFty_Output")
if not os.path.exists(NIFty_output_dir):
    os.mkdir(NIFty_output_dir)



# for each split, for each test
for split in splits:
    for i in range(tests):

        identifier = f"Khan_Unimputed_Split{split}_Test{i + 1}"
        SPG_samples_updated = SPG_samples.copy()
        St_samples_updated = St_samples.copy()

        # create the validation data
        validate_samples = sorted(random.sample(sorted(SPG_samples), num_samples_per_class_validation) + random.sample(sorted(St_samples), num_samples_per_class_validation))
        SPG_samples_updated.difference_update(validate_samples)
        St_samples_updated.difference_update(validate_samples)

        validate_quant = quant_table[quant_table['sample_id'].isin(validate_samples)].copy()
        validate_meta = meta_table[meta_table['sample_id'].isin(validate_samples)].copy()

        validate_quant_path = os.path.join(validate_output_dir, identifier + "_Validate_Quant.tsv")
        validate_meta_path = os.path.join(validate_output_dir, identifier + "_Validate_Meta.tsv")

        validate_quant.to_csv(validate_quant_path, sep="\t", index=False)
        validate_meta.to_csv(validate_meta_path, sep="\t", index=False)

        # create the FS data
        num_FS_samples = math.floor(split * fs_ratio)
        fs_samples = sorted(random.sample(sorted(SPG_samples_updated), num_FS_samples) + random.sample(sorted(St_samples_updated), num_FS_samples))
        SPG_samples_updated.difference_update(fs_samples)
        St_samples_updated.difference_update(fs_samples)

        fs_quant = quant_table[quant_table['sample_id'].isin(fs_samples)].copy()
        fs_meta = meta_table[meta_table['sample_id'].isin(fs_samples)].copy()

        fs_quant_path = os.path.join(fs_output_dir, identifier + "_FS_Quant.tsv")
        fs_meta_path = os.path.join(fs_output_dir, identifier + "_FS_Meta.tsv")

        fs_quant.to_csv(fs_quant_path, sep="\t", index=False)
        fs_meta.to_csv(fs_meta_path, sep="\t", index=False)

        # create the train/test data
        num_train_test_samples = math.ceil(split * train_test_ratio)
        train_test_samples = sorted(random.sample(sorted(SPG_samples_updated), num_train_test_samples) + random.sample(sorted(St_samples_updated), num_train_test_samples))
        SPG_samples_updated.difference_update(train_test_samples)
        St_samples_updated.difference_update(train_test_samples)

        train_test_quant = quant_table[quant_table['sample_id'].isin(train_test_samples)].copy()
        train_test_meta = meta_table[meta_table['sample_id'].isin(train_test_samples)].copy()

        train_test_quant_path = os.path.join(train_test_output_dir, identifier + "_Train_Test_Quant.tsv")
        train_test_meta_path = os.path.join(train_test_output_dir, identifier + "_Train_Test_Meta.tsv")

        train_test_quant.to_csv(train_test_quant_path, sep="\t", index=False)
        train_test_meta.to_csv(train_test_meta_path, sep="\t", index=False)

        # check that no samples overlapped between the three sets
        if set(validate_samples).intersection(set(fs_samples)) or set(validate_samples).intersection(set(train_test_samples)) or set(train_test_samples).intersection(set(fs_samples)):
            print("ERROR: overlapping samples")
            sys.exit()

        # create the NIFty output directory
        NIFty_output_path = os.path.join(NIFty_output_dir, identifier)
        if not os.path.exists(NIFty_output_path):
            os.mkdir(NIFty_output_path)

        # create the config file
        config_file_path = os.path.join(config_output_dir, identifier + "_Config.toml")

        with open(config_file_path, "w") as config:
            # project configs
            config.write("find_features = true\n")
            config.write("train_model = true\n")
            config.write("apply_model = false\n")
            config.write("seed = 'random'\n")
            config.write("input_files = 'individual'\n")

            # file configs
            config.write(f"output_dir = '{NIFty_output_path}'\n")
            config.write(f"feature_quant_file = '{fs_quant_path}'\n")
            config.write(f"feature_meta_file = '{fs_meta_path}'\n")
            config.write(f"train_quant_file = '{train_test_quant_path}'\n")
            config.write(f"train_meta_file = '{train_test_meta_path}'\n")
            config.write(f"validate_quant_file = '{validate_quant_path}'\n")
            config.write(f"validate_meta_file = '{validate_meta_path}'\n")

            # FS configs
            config.write("k_rules = 15\n")
            config.write("missingness_cutoff = 0.5\n")
            config.write("disjoint = false\n")
            config.write("mutual_information = true\n")
            config.write("mutual_information_cutoff = 0.7\n")

            # train/test configs
            config.write("impute_NA_missing = true\n")
            config.write("cross_val = 5\n")
            config.write("model_type = 'RF'\n")
            config.write("autotune_hyperparameters = ''\n")
            config.write("autotune_n_iter = 20\n")
            config.write("verbose = 0\n")
        



