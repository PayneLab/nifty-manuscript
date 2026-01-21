# nifty-manuscript
Contains the code and figures for the manuscript associated with NIFty.


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

### Incomplete Data
To recreate the results for testing on incomplete data, do the following:

1. Ensure you have the following python packages installed in your environment:
    * pandas
    * numpy
2. Download NIFty from <link to NIFy repo>.
2. Navigate to `Testing/No_Imputation/` and run the following python files:
    * Ai_imputed.py
    * Ai_unimputed.py
    * Furtwaengler_imputed_HSCxEarlyEryth.py
    * Furtwaengler_imputed_HSCxEMP.py
    * Furtwaengler_unimputed_HSCxEarlyEryth.py
    * Furtwaengler_unimputed_HSCxEMP.py
    * Khan_imputed.py
    * Khan_unimputed.py
    * Leduc_imputed.py
    * Leduc_unimputed.py
    * Montalvo_imputed.py
    * Montalvo_unimputed.py
    * Petrosius_imputed.py
    * Petrosius_unimputed.py
3. For each configuration file created (found in `Testing/No_Imputation/Test_{Dataset Identifier}/Config_Files`), run NIFty using the following command:

    `python <path_to_local_NIFty_download>/nifty.py -c <path to config file>`
    
4. Run `combine_results.py`.
