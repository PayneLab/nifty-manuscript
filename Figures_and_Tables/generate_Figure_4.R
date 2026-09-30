library(tidyverse)
library(this.path)

script_dir <- this.dir()
setwd(script_dir)


## RF - traditional
data <- read_tsv(file.path("..", "Testing", "Method_Comparison", "Random_Forest_Tests", "combined_results_random_forest.tsv"))

trad_rf_table <- data %>%
  group_by(Dataset, `Data Type`, `Cell Types`, `Samples per Class`) %>%
  summarize("Validation Accuracy" = mean(`Validation Accuracy`)) %>%
  mutate("Classification_Method" = "Traditional", 
         "Classifier" = "RF")



## SVM - traditional
data <- read_tsv(file.path("..", "Testing", "Method_Comparison", "SVM_Tests", "combined_results_svm.tsv"))

trad_svm_table <- data %>%
  group_by(Dataset, `Data Type`, `Cell Types`, `Samples per Class`) %>%
  summarize("Validation Accuracy" = mean(`Validation Accuracy`)) %>%
  mutate("Classification_Method" = "Traditional", 
         "Classifier" = "SVM")



## SVM - NIFty
data <- read_tsv(file.path("..", "Testing", "Method_Comparison", "MIFty_SVM_Tests", "combined_results_NIFty_SVM.tsv"))

svm_table <- data %>%
  group_by(Dataset, `Data Type`, `Cell Types`, `Samples per Class`) %>%
  summarize("Validation Accuracy" = mean(`Validation Accuracy`)) %>%
  mutate("Classification_Method" = "NIFty", 
         "Classifier" = "SVM")



## RF - NIFty
data <- read_tsv(file.path("..", "Testing", "No_Imputation", "combined_results.tsv"))

rf_table <- data %>%
  filter(`Samples per Class` == 50) %>%
  group_by(Dataset, `Data Type`, `Cell Types`, `Samples per Class`) %>%
  summarize("Validation Accuracy" = mean(`Validation Accuracy`)) %>%
  mutate("Classification_Method" = "NIFty", 
         "Classifier" = "RF")



full_dataset <- rf_table %>% 
  full_join(svm_table) %>% 
  full_join(trad_rf_table) %>% 
  full_join(trad_svm_table) %>%
  mutate("Identifier" = ifelse(!is.na(`Cell Types`), paste0(Dataset, "_", `Cell Types`), Dataset)) %>%
  mutate(Identifier = ifelse(Identifier == "Montalvo", 
                             "Montalvo Landivar", 
                             Identifier)) %>%
  mutate(Identifier = str_replace(Identifier, "Furtwaengler", "Furtwängler"))




## plot the data
ggplot(data = full_dataset, aes(
    x = as.numeric(factor(Identifier)) +
      ifelse(Classification_Method == "Traditional", -0.2, 0.2),
    y = `Validation Accuracy`,
    color = Classifier,
    alpha = Classification_Method,
    group = interaction(Identifier, Classifier)
  )) +
  geom_line() +
  geom_point() +
  scale_alpha_manual(values = c("Traditional" = 0.4, "NIFty" = 1)) +
  scale_color_manual(values = c("RF" = "#008080", "SVM" = "#D11A5B")) + 
  scale_x_continuous(
    breaks = seq_along(unique(full_dataset$Identifier)),
    labels = unique(full_dataset$Identifier)
  ) +
  facet_wrap(~`Data Type`) +
  labs(alpha = "Classification Method", x = "Dataset", y = "Average Validation Accuracy") + 
  ylim(0, 1) + 
  theme_bw() + 
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1), 
        panel.grid.minor.x = element_blank())

ggsave("Fig4.png", width = 7.5, height = 4.5, units = "in", dpi = 600)
