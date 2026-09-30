#!/bin/usr/env python
import pandas as pd
import numpy as np
import tomllib
import sys
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.inspection import permutation_importance
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, roc_auc_score


def parse_configs(config_file_path):
    print("PARSING CONFIGS", file=sys.stderr, flush=True)

    with open(config_file_path, "rb") as f:
        configs = tomllib.load(f)
    return configs


def load_aligned_pair(quant_path, meta_path):
    quant = pd.read_csv(quant_path, sep="\t")
    meta = pd.read_csv(meta_path, sep="\t")

    if not quant["sample_id"].is_unique:
        print(f"Duplicate sample IDs in {quant_path}")
        sys.exit()

    if not meta["sample_id"].is_unique:
        print(f"Duplicate sample IDs in {meta_path}")
        sys.exit()

    if set(quant["sample_id"]) != set(meta["sample_id"]):
        raise ValueError(
            f"Sample ID sets do not match:\n"
            f"Quant-only: {set(quant['sample_id']) - set(meta['sample_id'])}\n"
            f"Meta-only: {set(meta['sample_id']) - set(quant['sample_id'])}"
        )

    quant = quant.sort_values("sample_id").reset_index(drop=True)
    meta = meta.sort_values("sample_id").reset_index(drop=True)

    if not quant["sample_id"].equals(meta["sample_id"]):
        print("Quantification and metadata rows are not aligned")
        sys.exit()

    return quant, meta


def filter_proteins(quant):
    print("FILTERING PROTEINS", file=sys.stderr, flush=True)

    quant_filtered = quant.dropna(axis=1)
    print(f"INFO: {len(quant.columns) - 1} proteins before filtering.", file=sys.stderr, flush=True)
    print(f"INFO: {len(quant_filtered.columns) - 1} proteins after filtering.", file=sys.stderr, flush=True)
    return quant_filtered


def select_features(fs_quant, fs_meta, N, verbose):
    print("SELECTING FEATURES", file=sys.stderr, flush=True)

    X = fs_quant
    y = fs_meta["classification_label"].tolist()

    rf = RandomForestClassifier(verbose=verbose)
    rf.fit(X, y)
    permutation = permutation_importance(rf, X, y, n_repeats=5, scoring="roc_auc", n_jobs=-1)

    importances = pd.DataFrame({
    "Protein": fs_quant.columns,
    "Importance_Mean": permutation.importances_mean,
    "Importance_SD": permutation.importances_std
    })

    importances = importances.sort_values(
    "Importance_Mean",
    ascending=False
    )

    selected_features = importances.head(N)["Protein"].tolist()

    return selected_features


def train_model(tt_quant, tt_meta, verbose, cross_val):
    print("TRAINING MODEL", file=sys.stderr, flush=True)
    """Trains a classifier and returns the cv score and model."""

    scoring = {
        'Accuracy': make_scorer(accuracy_score),
        'Precision': make_scorer(precision_score, average='weighted'),
        'Recall': make_scorer(recall_score, average='weighted')
    }

    X = tt_quant
    y = tt_meta['classification_label'].tolist()

    rf = RandomForestClassifier(verbose=verbose)

    cv = cross_validate(rf, X, y, cv=cross_val, scoring=scoring, verbose=verbose)
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
    return rf, model_information


def validate_model(model, val_quant, val_meta):
    print("VALIDATING MODEL", file=sys.stderr, flush=True)

    X_val = val_quant
    y_val = val_meta['classification_label'].tolist()
    y_val_pred = model.predict(X_val)
    val_accuracy = accuracy_score(y_val, y_val_pred)
    val_precision = precision_score(y_val, y_val_pred, average='weighted')
    val_recall = recall_score(y_val, y_val_pred, average='weighted')

    val_scores = {
        'Accuracy': val_accuracy, 
        'Precision': val_precision, 
        'Recall': val_recall
    }
    return val_scores


def save_model_information(metrics, output_file_path):
    print("SAVING MODEL", file=sys.stderr, flush=True)

    with open(output_file_path, "w") as out_file:
        # save model parameters
        out_file.write("---MODEL PARAMETERS---\n")
        for param, value in metrics['params'].items():
            out_file.write(f"{param}: {value}\n")

        # save train/test scores
        out_file.write("\n---TRAIN/TEST CV SCORES---\n")
        for score, value in metrics['cv_scores'].items():
            out_file.write(f"{score}: {value}\n")
                            
        # save validation scores
        out_file.write("\n---VALIDATION SCORES---\n")
        for score, value in metrics['val_scores'].items():
            out_file.write(f"{score}: {value}\n")
    print(f"INFO: Model information saved to '{output_file_path}'.", file=sys.stderr, flush=True)



# read in configs and data
config_file_path = sys.argv[1]
configs = parse_configs(config_file_path)

fs_quant, fs_meta = load_aligned_pair(configs["feature_quant_file"], configs["feature_meta_file"])

tt_quant, tt_meta = load_aligned_pair(configs["train_quant_file"], configs["train_meta_file"])

val_quant, val_meta = load_aligned_pair(configs["validate_quant_file"], configs["validate_meta_file"])


# filter proteins with NA values
fs_quant_filtered = filter_proteins(fs_quant).drop(columns='sample_id')
tt_quant_filtered = filter_proteins(tt_quant).drop(columns='sample_id')
val_quant_filtered = filter_proteins(val_quant).drop(columns='sample_id')

common_proteins = list(set(fs_quant_filtered.columns).intersection(tt_quant_filtered.columns, val_quant_filtered.columns))

fs_quant_filtered = fs_quant_filtered[common_proteins]
print(fs_quant_filtered.shape)


# select features using permutation importance
selected_proteins = select_features(fs_quant_filtered, fs_meta, int(configs["n_features"]), int(configs["verbose"]))


# train/test model
tt_quant_filtered = tt_quant_filtered[selected_proteins]
model, model_information = train_model(tt_quant_filtered, tt_meta, int(configs["verbose"]), int(configs["cross_val"]))


# validate model
val_quant_filtered = val_quant_filtered[selected_proteins]
model_information['val_scores'] = validate_model(model, val_quant_filtered, val_meta)


# output hyperparameters, train/test metrics, and validation metrics
output_file_path = os.path.join(configs["output_dir"], "model_information.txt")
save_model_information(model_information, output_file_path)

