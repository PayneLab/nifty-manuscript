#!bin/usr/env python
import os
import sys
import random
import math
import subprocess
import pandas as pd
from pathlib import Path
import sklearn

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score

nifty_directory = ""  # ADD PATH TO nifty.py AND OTHER DEPENDENCIES HERE
sys.path.append(nifty_directory)

from DataTransformer import DataTransformer

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)


# input files
quant_file = os.path.join(script_directory, os.pardir, os.pardir, 'Data_Prep', 'Ai_Van-Eyk_2025', 'NIFty_Ready_Data', 'quant_unimputed.tsv')
meta_file = os.path.join(script_directory, os.pardir, os.pardir, 'Data_Prep', 'Ai_Van-Eyk_2025', 'NIFty_Ready_Data', 'meta.tsv')

quant_table = pd.read_csv(quant_file, sep='\t')
meta_table = pd.read_csv(meta_file, sep='\t')

day0_samples = set(meta_table[meta_table['classification_label'] == "day0"]['sample_id'].tolist())
day2_samples = set(meta_table[meta_table['classification_label'] == "day2"]['sample_id'].tolist())
day4_samples = set(meta_table[meta_table['classification_label'] == "day4"]['sample_id'].tolist())
day10_samples = set(meta_table[meta_table['classification_label'] == "day10"]['sample_id'].tolist())
day21_samples = set(meta_table[meta_table['classification_label'] == "day21"]['sample_id'].tolist())

# print(meta_table['classification_label'].value_counts())


# set up testing information
tests = 100
num_samples_per_class_fs = 50
num_samples_per_class_train_test = 100
num_samples_per_class_validate = 50


# create the directories for files information
output_dir = os.path.join(script_directory, "Test_Ai_Multiclass")
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


for i in range(100):
    identifier = f"Test_{i}"
    main_output_dir = os.path.join(output_dir, identifier)
    if not os.path.exists(main_output_dir):
        os.mkdir(main_output_dir)

    NIFty_output_dir = os.path.join(main_output_dir, "NIFty_Output")
    if not os.path.exists(NIFty_output_dir):
        os.mkdir(NIFty_output_dir)


    # split the data
    day0_samples_updated = day0_samples.copy()
    day2_samples_updated = day2_samples.copy()
    day4_samples_updated = day4_samples.copy()
    day10_samples_updated = day10_samples.copy()
    day21_samples_updated = day21_samples.copy()

    # create the validate data
    validate_samples = random.sample(sorted(day0_samples), num_samples_per_class_validate)
    validate_samples += random.sample(sorted(day2_samples), num_samples_per_class_validate)
    validate_samples += random.sample(sorted(day4_samples), num_samples_per_class_validate)
    validate_samples += random.sample(sorted(day10_samples), num_samples_per_class_validate)
    validate_samples += random.sample(sorted(day21_samples), num_samples_per_class_validate)
    validate_samples.sort()

    day0_samples_updated.difference_update(validate_samples)
    day2_samples_updated.difference_update(validate_samples)
    day4_samples_updated.difference_update(validate_samples)
    day10_samples_updated.difference_update(validate_samples)
    day21_samples_updated.difference_update(validate_samples)

    validate_quant = quant_table[quant_table['sample_id'].isin(validate_samples)].copy()
    validate_meta = meta_table[meta_table['sample_id'].isin(validate_samples)].copy()

    validate_quant_path = os.path.join(main_output_dir, "Validate_Quant.tsv")
    validate_meta_path = os.path.join(main_output_dir, "Validate_Meta.tsv")

    validate_quant.to_csv(validate_quant_path, sep="\t", index=False)
    validate_meta.to_csv(validate_meta_path, sep="\t", index=False)

    validate_quant.set_index('sample_id', inplace=True)
    # print(validate_quant)

    # create the fs data
    fs_samples = random.sample(sorted(day0_samples_updated), num_samples_per_class_fs)
    fs_samples += random.sample(sorted(day2_samples_updated), num_samples_per_class_fs)
    fs_samples += random.sample(sorted(day4_samples_updated), num_samples_per_class_fs)
    fs_samples += random.sample(sorted(day10_samples_updated), num_samples_per_class_fs)
    fs_samples += random.sample(sorted(day21_samples_updated), num_samples_per_class_fs)
    fs_samples.sort()

    day0_samples_updated.difference_update(fs_samples)
    day2_samples_updated.difference_update(fs_samples)
    day4_samples_updated.difference_update(fs_samples)
    day10_samples_updated.difference_update(fs_samples)
    day21_samples_updated.difference_update(fs_samples)

    fs_quant = quant_table[quant_table['sample_id'].isin(fs_samples)].copy()
    fs_meta = meta_table[meta_table['sample_id'].isin(fs_samples)].copy()

    fs_quant_path = os.path.join(main_output_dir, f"FS_Quant.tsv")

    fs_quant.to_csv(fs_quant_path, sep="\t", index=False)

    # create the train_test data
    train_test_samples = random.sample(sorted(day0_samples_updated), num_samples_per_class_train_test)
    train_test_samples += random.sample(sorted(day2_samples_updated), num_samples_per_class_train_test)
    train_test_samples += random.sample(sorted(day4_samples_updated), num_samples_per_class_train_test)
    train_test_samples += random.sample(sorted(day10_samples_updated), num_samples_per_class_train_test)
    train_test_samples += random.sample(sorted(day21_samples_updated), num_samples_per_class_train_test)
    train_test_samples.sort()

    day0_samples_updated.difference_update(train_test_samples)
    day2_samples_updated.difference_update(train_test_samples)
    day4_samples_updated.difference_update(train_test_samples)
    day10_samples_updated.difference_update(train_test_samples)
    day21_samples_updated.difference_update(train_test_samples)

    train_test_quant = quant_table[quant_table['sample_id'].isin(train_test_samples)].copy()
    train_test_meta = meta_table[meta_table['sample_id'].isin(train_test_samples)].copy()

    train_test_quant_path = os.path.join(main_output_dir, "Train_Test_Quant.tsv")
    train_test_meta_path = os.path.join(main_output_dir, "Train_Test_Meta.tsv")

    train_test_quant.to_csv(train_test_quant_path, sep="\t", index=False)
    train_test_meta.to_csv(train_test_meta_path, sep="\t", index=False)

    train_test_quant.set_index('sample_id', inplace=True)
    # print(train_test_quant)


    # check that no samples overlapped between the three sets
    if set(validate_samples).intersection(set(train_test_samples)) or set(validate_samples).intersection(set(fs_samples)) or set(fs_samples).intersection(set(train_test_samples)):
        print("ERROR: overlapping samples")
        sys.exit()


    # for each class, read in the fs data and mask the other 4 classes to "other"
    #   run nifty to get the top 5 pairs
    classes = meta_table['classification_label'].unique().tolist()
    # print(classes)

    script_path = os.path.join(main_output_dir, f"run_Ai_multiclass.sh")
    with open(script_path, "w") as script:
        pass

    feature_dirs = []

    for cls in classes:
        # mask other cell types to "other"
        cls_meta = fs_meta.copy()
        cls_meta.loc[cls_meta['classification_label'] != cls, 'classification_label'] = "other"

        # print(fs_meta['classification_label'].value_counts())
        # print(cls_meta['classification_label'].value_counts())

        # save the meta data
        fs_meta_path = os.path.join(main_output_dir, f"FS_{cls}_Meta.tsv")

        cls_meta.to_csv(fs_meta_path, sep="\t", index=False)


        # create the config file
        config_file_path = os.path.join(main_output_dir, f"Config_{cls}.toml")
        NIFty_output_path = os.path.join(NIFty_output_dir, f"Test_{cls}_vs_Others")

        if not os.path.exists(NIFty_output_path):
            os.mkdir(NIFty_output_path)

        feature_dirs.append(NIFty_output_path)

        with open(config_file_path, "w") as config:
            # project configs
            config.write("find_features = true\n")
            config.write("train_model = false\n")
            config.write("apply_model = false\n")
            config.write("seed = 'random'\n")
            config.write("input_files = 'reference'\n")

            # file configs
            config.write(f"output_dir = '{NIFty_output_path}'\n")
            config.write(f"reference_quant_file = '{fs_quant_path}'\n")
            config.write(f"reference_meta_file = '{fs_meta_path}'\n")
            config.write(f"feature_quant_file = ''\n")
            config.write(f"feature_meta_file = ''\n")
            config.write(f"train_quant_file = ''\n")
            config.write(f"train_meta_file = ''\n")
            config.write(f"validate_quant_file = ''\n")
            config.write(f"validate_meta_file = ''\n")

            # FS configs
            config.write("k_rules = 5\n")
            config.write("missingness_cutoff = 0.5\n")
            config.write("disjoint = false\n")
            config.write("mutual_information = true\n")
            config.write("mutual_information_cutoff = 0.7\n")

        # add command to bash file
        NIFty_cmd = f"python /fslhome/nitz1bug/PayneLab/NIFty_Testing/MANUSCRIPT/nifty.py -c {config_file_path}"
        with open(script_path, "a") as script:
            script.write(f"{NIFty_cmd}\n")


    # run job to get features
    terminal_cmd = f"sh {script_path}"
    os.system(terminal_cmd)


    # read in the features to one list
    protein1 = []
    protein2 = []

    for feature_dir in feature_dirs:
        feature_file = os.path.join(feature_dir, "selected_features.tsv")

        features = pd.read_csv(feature_file, sep="\t")

        protein1.extend(features['Protein1'].tolist())
        protein2.extend(features['Protein2'].tolist())

    pairs = list(zip(protein1, protein2))
    # print(len(pairs))
    pairs = set(pairs)
    # print(len(pairs))

    pairs = pd.DataFrame(pairs, columns=['Protein1', 'Protein2'])
    # print(pairs)


    # reformat train_test quant table into binary table
    data_transformer = DataTransformer()
    train_test_quant = data_transformer.add_missing_proteins(feature_df=pairs, quant_df=train_test_quant)
    # print(train_test_quant)

    train_test_bool_dict = data_transformer.transform_df(feature_df=pairs, quant_df=train_test_quant)
    train_test_matrix = data_transformer.prep_vectorized_pairs_for_scikitlearn(feature_df=pairs, bool_dict=train_test_bool_dict)
    train_test_matrix.index = train_test_quant.index.copy()
    # print(train_test_matrix)


    # train a classifier
    scoring = {
                'Accuracy': make_scorer(accuracy_score),
                'Precision': make_scorer(precision_score, average='weighted'),
                'Recall': make_scorer(recall_score, average='weighted')
            }

    X = train_test_matrix
    y = train_test_meta['classification_label'].tolist()
    rf = RandomForestClassifier(verbose=0)
    cv = cross_validate(rf, X, y, cv=5, scoring=scoring, verbose=0)
    cv_scores = {
        'Accuracy_Mean': cv['test_Accuracy'].mean(), 
        'Accuracy_Std': cv['test_Accuracy'].std(), 
        'Precision_Mean': cv['test_Precision'].mean(), 
        'Precision_Std': cv['test_Precision'].std(), 
        'Recall_Mean': cv['test_Recall'].mean(), 
        'Recall_Std': cv['test_Recall'].std()
    }
    rf.fit(X, y)
    params = rf.get_params()

    model_information = {
                    'cv_scores': cv_scores, 
                    'params': params
                }

    # print(model_information)
    output_file_path = os.path.join(main_output_dir, "model_information.txt")
    with open(output_file_path, "w") as out_file:
        # save model parameters
        out_file.write("---MODEL PARAMETERS---\n")
        for param, value in model_information['params'].items():
            out_file.write(f"{param}: {value}\n")

        # save train/test scores
        out_file.write("\n---TRAIN/TEST CV SCORES---\n")
        for score, value in model_information['cv_scores'].items():
            out_file.write(f"{score}: {value}\n")


    # reformat train_test quant table into binary table
    validate_quant = data_transformer.add_missing_proteins(feature_df=pairs, quant_df=validate_quant)
    # print(validate_quant)

    validate_bool_dict = data_transformer.transform_df(feature_df=pairs, quant_df=validate_quant)
    validate_matrix = data_transformer.prep_vectorized_pairs_for_scikitlearn(feature_df=pairs, bool_dict=validate_bool_dict)
    validate_matrix.index = validate_quant.index.copy()
    # print(validate_matrix)


    # validate the classifier
    predictions = rf.predict(validate_matrix)


    # save the validate predictions
    index = validate_quant.index.copy()

    formatted_predictions = pd.DataFrame({
        'sample_id': index, 
        'predicted_classification_label': predictions
    })

    # print(validate_meta)
    # print(formatted_predictions)

    merged_information = validate_meta.merge(formatted_predictions)
    # print(merged_information)
    output_file_path = os.path.join(main_output_dir, "predictions.tsv")
    merged_information.to_csv(output_file_path, sep='\t')
