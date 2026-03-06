# nifty-manuscript
Contains the code and figures for the manuscript associated with NIFty.

Download or clone the repository before continuing.


## Data Prep
To download and prepare the manuscript datasets for NIFty, do the following:

1. Ensure you have the following python packages installed in your environment:
    * pandas
    * numpy
    * scikit-learn
    * anndata
    * pyarrow
2. Navigate to `Data_Prep/Ai_Van-Eyk_2025/Original_Data/README.md` and follow the instructions.
3. Navigate to `Data_Prep/Furtwaengler_Porse_Schoof_2025/Original_Data/README.md` and follow the instructions.
4. Navigate to `Data_Prep/Khan_Elcheikhali_Slavov_2024/Original_Data/README.md` and follow the instructions.
5. Navigate to `Data_Prep/Leduc_Slavov_2022/Original_Data/README.md` and follow the instructions.
6. Navigate to `Data_Prep/Montalvo_Alvarez-Dominguez_Slavov_2023/Original_Data/README.md` and follow the instructions.
7. Navigate to `Data_Prep/Petrosius_Schoof_2025/Original_Data/README.md` and follow the instructions.


## Testing
If you have not already, follow the instructions in the `Data Prep` section before continuing.

### Incomplete Data
To recreate the results for testing on incomplete data, do the following:

1. Ensure you have the following python packages installed in your environment:
    * pandas
    * numpy
2. Download NIFty from <link to NIFy repo> and install the dependencies as described in the documentation.
3. Navigate to `Testing/No_Imputation/` and run the following python files:
    * `Ai_imputed.py`
    * `Ai_unimputed.py`
    * `Furtwaengler_imputed_HSCxEarlyEryth.py`
    * `Furtwaengler_imputed_HSCxEMP.py`
    * `Furtwaengler_unimputed_HSCxEarlyEryth.py`
    * `Furtwaengler_unimputed_HSCxEMP.py`
    * `Khan_imputed.py`
    * `Khan_unimputed.py`
    * `Leduc_imputed.py`
    * `Leduc_unimputed.py`
    * `Montalvo_imputed.py`
    * `Montalvo_unimputed.py`
    * `Petrosius_imputed.py`
    * `Petrosius_unimputed.py`
4. For each configuration file created (found in `Testing/No_Imputation/Test_{Dataset Identifier}/Config_Files`), run NIFty using the following command:

    `python <path_to_local_NIFty_download>/nifty.py -c <path to config file>`

5. Run `combine_results.py` (this will replace `combined_results.tsv` with your results).

### Batch Effects
Upcoming

### Multiclass
To recreate the results for testing on multiclass data, do the following:

1. Ensure you have the following python packages installed in your environment:
    * pandas
    * scikit-learn
2. Download NIFty from <link to NIFy repo> and install the dependencies as described in the documentation.
3. Navigate to `Testing/Multiclass/`.
4. Add the absolute path to the directory containing `nifty.py` and associated files to line 18 in `multiclass_wrapper.py`.
5. Run `multiclass_wrapper.py`.
6. Run `combine_predictions.py` (this will replace `combined_predictions.tsv` with your results).

## Figures and Tables
You need to have completed the `Data Prep` and `Testing` sections before continuing.

To recreate Figures 3, 4, and 6 and Table 1 found in the manuscript, do the following:

1. Ensure you have the following R packages installed in your environment:
    * tidyverse
    * this.path
    * caret
    * ggtext
2. Navigate to `Figures_and_Tables`. 
3. Run the following R files:
    * `generate_Figure_3.R` (recreates `Fig3_Leduc.png`, `Fig3_Montalvo.png`)
    * `generate_Table_1.R` (recreates `Table1.tsv`)
    * *Figure 4 Upcoming*
    * `generate_Figure_6.R` (recreates `Fig6.png`)

