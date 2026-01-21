library(tidyverse)
library(this.path)

script_dir <- this.dir()
setwd(script_dir)

data <- read_tsv(file.path("..", "Testing", "No_Imputation", "combined_results.tsv"))

table <- data %>%
  filter((`Samples per Class` == 100) | (`Samples per Class` == 50)) %>%
  group_by(Dataset, `Data Type`, `Cell Types`, `Samples per Class`) %>%
  summarize("Validation Accuracy" = mean(`Validation Accuracy`)) %>%
  unite("Test", `Data Type`, `Samples per Class`, sep = "_") %>%
  pivot_wider(names_from = Test, values_from = `Validation Accuracy`)

write_tsv(table, "Table1.tsv")


