library(tidyverse)
library(ggnewscale)


data_n_norm <- read_tsv("..", "Testing", "Batch_Effects", "combined_results_non-normalized.tsv")
data_norm <- read_tsv("..", "Testing", "Batch_Effects", combined_results_normalized.tsv")



plot_data_n_norm <- data_n_norm %>%
  group_by(Dataset, `Test Category`) %>%
  summarize(Average_Accuracy = mean(`Validation Accuracy`)) %>%
  ungroup() %>%
  mutate(`Test Category` = factor(`Test Category`, levels=c("control", 1, 2, 3, 4, 5, 6, 7))) %>%
  mutate("Normalized" = FALSE)

plot_data_norm <- data_norm %>%
  group_by(Dataset, `Test Category`) %>%
  summarize(Average_Accuracy = mean(`Validation Accuracy`)) %>%
  ungroup() %>%
  mutate(`Test Category` = factor(`Test Category`, levels=c("control", 1, 2, 3, 4, 5, 6, 7))) %>%
  mutate("Normalized" = TRUE)



plot_data <- full_join(plot_data_norm, plot_data_n_norm) %>%
  mutate(
    Point_Color = ifelse(Normalized, "#F28E8E", "#6BAED6"),  # light
    Summary_Color = ifelse(Normalized, "#8B0000", "#08306B") # dark
  )

ggplot(plot_data, aes(x = `Test Category`, y = Average_Accuracy)) +
  # Points
  geom_jitter(
    aes(color = Point_Color),
    position = position_jitterdodge(jitter.width = 0.5, dodge.width = 0.7),
    alpha = 0.5,
    size = 2
  ) +
  # Error bars
  stat_summary(
    aes(color = Summary_Color, group = Normalized),
    fun.data = mean_sdl,
    fun.args = list(mult = 1),
    geom = "errorbar",
    width = 0.2,
    size = 1
  ) +
  # Mean points
  stat_summary(
    aes(color = Summary_Color, group = Normalized),
    fun = mean,
    geom = "point",
    size = 4
  ) +
  # Mean lines
  stat_summary(
    aes(color = Summary_Color, group = Normalized),
    fun = mean,
    geom = "line",
    size = 1
  ) +
  # Identity scale
  scale_color_identity(
    name = "Data Type", 
    breaks = c("#08306B", "#8B0000"), 
    labels = c("Non-Normalized", "Normalized"), 
    guide = "legend"
  ) +
  theme_bw(base_size = 18) +
  ylim(c(0, 1.05)) + 
  labs(x = "Number of Batches in FS and Model Training", y = "Average Validation Accuracy")

ggsave("Fig4.png", width = 10, height = 6, units = "in", dpi = 600)




plot_data %>% 
  mutate(Normalized = ifelse(Normalized == TRUE, "Normalized", "Non-Normalized")) %>%
  group_by(`Test Category`, Normalized) %>%
  summarize(average_accuracy = mean(Average_Accuracy), 
            sd_accuracy = sd(Average_Accuracy)) %>%
  View()


