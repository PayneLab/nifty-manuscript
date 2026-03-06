library(tidyverse)
library(this.path)

script_dir <- this.dir()
setwd(script_dir)

data <- read_tsv(file.path("..", "Testing", "No_Imputation", "incomplete_protein_analysis_results.tsv"))

## Complete Protein Analysis
data %>% 
  filter(`Samples per Class` == 50) %>%
  pull(Proportion_Complete_Proteins) %>%
  unique() %>%
  max()

data %>% 
  filter(`Samples per Class` == 100) %>%
  pull(Proportion_Complete_Proteins) %>%
  unique() %>%
  max()

data %>% 
  filter(`Samples per Class` == 50) %>%
  pull(Proportion_Complete_Proteins) %>%
  unique() %>%
  min()

data %>% 
  filter(`Samples per Class` == 100) %>%
  pull(Proportion_Complete_Proteins) %>%
  unique() %>%
  min()

data %>% 
  pull(Proportion_Complete_Proteins) %>%
  median()

data %>% 
  pull(Proportion_Complete_Proteins) %>%
  IQR()



## Complete Pair Analysis
data %>% 
  filter(`Samples per Class` == 50) %>%
  pull(Proportion_Complete_Pairs) %>%
  unique() %>%
  max()

data %>% 
  filter(`Samples per Class` == 100) %>%
  pull(Proportion_Complete_Pairs) %>%
  unique() %>%
  max()

data %>% 
  filter(`Samples per Class` == 50) %>%
  pull(Proportion_Complete_Pairs) %>%
  unique() %>%
  min()

data %>% 
  filter(`Samples per Class` == 100) %>%
  pull(Proportion_Complete_Pairs) %>%
  unique() %>%
  min()

data %>% 
  pull(Proportion_Complete_Pairs) %>%
  median()

data %>% 
  pull(Proportion_Complete_Pairs) %>%
  IQR()


  