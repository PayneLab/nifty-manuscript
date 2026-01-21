library(tidyverse)
library(caret)
library(ggtext)
library(this.path)

script_dir <- this.dir()
setwd(script_dir)

data <- read_tsv(file.path("..", "Testing", "Multiclass", "combined_predictions.tsv")) %>%
  mutate(predicted_classification_label = factor(predicted_classification_label, levels=c("day0", "day2", "day4", "day10", "day21"))) %>%
  mutate(predicted_classification_label = fct_recode(predicted_classification_label, "Day 0" = "day0", "Day 2" = "day2", "Day 4" = "day4", "Day 10" = "day10", "Day 21" = "day21")) %>%
  mutate(classification_label = factor(classification_label, levels=c("day0", "day2", "day4", "day10", "day21"))) %>%
  mutate(classification_label = fct_recode(classification_label, "Day 0" = "day0", "Day 2" = "day2", "Day 4" = "day4", "Day 10" = "day10", "Day 21" = "day21"))


# create one confusion matrix per test
cm_list <- data %>%
  group_by(test) %>%
  group_map(~{
    cm <- confusionMatrix(factor(.x$predicted_classification_label), factor(.x$classification_label))
    as.data.frame(cm$table)  # table contains counts
  })

# combine into one table
cm_long <- bind_rows(cm_list, .id = "Test") %>%
  group_by(Reference, Prediction) %>%
  summarise(
    mean_count = mean(Freq),
    sd_count = sd(Freq),
    .groups = "drop"
  ) %>%
  mutate(mean_percent = mean_count / 50 * 100, 
         sd_percent = sd_count / 50 * 100) %>%
  mutate(mean_label = paste0(round(mean_percent, 2), "%"),
         sd_label = paste0("(+/-", round(sd_percent, 2), "%)"))

# plot
ggplot(data = cm_long, aes(x = Prediction, y = Reference, fill = mean_percent)) +
  geom_tile() +
  geom_text(aes(label = mean_label), nudge_y = 0.1, size = 4) +
  geom_text(aes(label = sd_label), nudge_y = -0.15, size = 2.5) +
  scale_fill_gradient(low = "white", high = "steelblue", limit = c(0, 100), breaks = c(0, 25, 50, 75, 100)) +
  labs(x = "Predicted Label", y = "Actual Label", fill = "Mean %\n") +
  theme_bw()

ggsave("Fig5.png", width = 5, height = 4, units = "in", dpi = 600)

