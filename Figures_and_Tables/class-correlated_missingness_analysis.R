library(tidyverse)
library(this.path)

script_dir <- this.dir()
setwd(script_dir)

missingness_prop_cutoff = 0.5

data <- read_tsv(file.path("..", "Testing", "No_Imputation", "class-correlated_missingness_analysis_results.tsv"))

no_imp_data <- data %>%
  mutate("Missingness A - B" = `Missingness Class A` - `Missingness Class B`) %>%
  mutate("Missingness Difference" = abs(`Missingness A - B`))

## Proportion of rules with class-correlated missingness by dataset
no_imp_plot_data <- no_imp_data %>%
  group_by(Dataset, `Data Type`, `Cell Types`, `Samples per Class`, Test) %>%
  summarize("Proportion Missingness" = mean(`Missingness Difference` > missingness_prop_cutoff)) %>%
  mutate("Label" = ifelse(!is.na(`Cell Types`), paste0(Dataset, "_", `Cell Types`), Dataset)) %>%
  mutate(Dataset = as_factor(Dataset)) %>%
  mutate(`Samples per Class` = as_factor(`Samples per Class`))

no_imp_plot_data %>% 
  group_by(Dataset, `Samples per Class`) %>%
  summarize("Median Proportion" = median(`Proportion Missingness`)) %>%
  mutate("Rules out of 15" = `Median Proportion` * 15) %>%
  View()

ggplot(data = no_imp_plot_data, mapping = aes(x = Label, y = `Proportion Missingness`, color = `Samples per Class`, fill = `Samples per Class`, group = interaction(Label, `Samples per Class`))) + 
  geom_boxplot(position = position_dodge(width = 0.45),
               width = 0.30,
               alpha = 0.25) +
  scale_color_manual(values = c("50" = "#7B3294", "100" = "#008837"),
                     name = "Samples per Class") +
  scale_fill_manual(values = c("50" = "#7B3294", "100" = "#008837"), 
                    name = "Samples per Class") +
  labs(x = "Dataset", y = "Proportion of Rules Driven by\nClass-Correlated Missingness") +
  theme_bw() + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1))







