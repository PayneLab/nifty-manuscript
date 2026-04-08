library(tidyverse)
library(this.path)

script_dir <- this.dir()
setwd(script_dir)

data <- read_tsv(file.path("..", "Testing", "No_Imputation", "combined_results.tsv"))

montalvo_imputed_data <- data %>%
  filter(Dataset == "Montalvo") %>%
  filter(`Data Type` == "Imputed") %>%
  mutate(`Samples per Class` = factor(`Samples per Class`))

montalvo_unimputed_data <- data %>%
  filter(Dataset == "Montalvo") %>%
  filter(`Data Type` == "Unimputed") %>%
  mutate(`Samples per Class` = factor(`Samples per Class`))

leduc_imputed_data <- data %>%
  filter(Dataset == "Leduc")%>%
  filter(`Data Type` == "Imputed") %>%
  mutate(`Samples per Class` = factor(`Samples per Class`))

leduc_unimputed_data <- data %>%
  filter(Dataset == "Leduc")%>%
  filter(`Data Type` == "Unimputed") %>%
  mutate(`Samples per Class` = factor(`Samples per Class`))





# plot Montalvo et al
plot_data_montalvo <- full_join(montalvo_imputed_data, montalvo_unimputed_data) %>%
  mutate(
    Point_Color = ifelse(`Data Type` == "Imputed", "#FDC086", "#80CDC1"),
    Summary_Color = ifelse(`Data Type` == "Imputed", "#BF5B17", "#018571")
  )

ggplot(plot_data_montalvo, aes(x = `Samples per Class`, y = `Validation Accuracy`)) +
  # Points
  geom_jitter(
    aes(color = Point_Color, group = `Data Type`),
    position = position_jitterdodge(jitter.width = 0.5, dodge.width = 0.7),
    alpha = 0.5,
    size = 2
  ) +
  # Error bars
  stat_summary(
    aes(color = Summary_Color, group = `Data Type`),
    fun.data = mean_sdl,
    fun.args = list(mult = 1),
    geom = "errorbar",
    width = 0.2,
    size = 1
  ) +
  # Mean points
  stat_summary(
    aes(color = Summary_Color, group = `Data Type`),
    fun = mean,
    geom = "point",
    size = 4
  ) +
  # Mean lines
  stat_summary(
    aes(color = Summary_Color, group = `Data Type`),
    fun = mean,
    geom = "line",
    size = 1
  ) +
  # Identity scale
  scale_color_identity(
    name = "Data Type", 
    breaks = c("#BF5B17", "#018571"), 
    labels = c("Imputed", "Unimputed"), 
    guide = "legend"
  ) +
  theme_bw(base_size = 18) +
  ylim(c(0, 1.05)) + 
  labs(x = "Total Samples per Class\n(before Splitting for FS [30%] and Train/Test [70%])", 
       y = "Validation Accuracy")
ggsave("Fig3_montalvo.png", width = 10, height = 6, units = "in", dpi = 600)




# plot leduc et al
plot_data_leduc <- full_join(leduc_imputed_data, leduc_unimputed_data) %>%
  mutate(
    Point_Color = ifelse(`Data Type` == "Imputed", "#FDC086", "#80CDC1"),
    Summary_Color = ifelse(`Data Type` == "Imputed", "#BF5B17", "#018571")
  )

ggplot(plot_data_leduc, aes(x = `Samples per Class`, y = `Validation Accuracy`)) +
  # Points
  geom_jitter(
    aes(color = Point_Color, group = `Data Type`),
    position = position_jitterdodge(jitter.width = 0.5, dodge.width = 0.7),
    alpha = 0.5,
    size = 2
  ) +
  # Error bars
  stat_summary(
    aes(color = Summary_Color, group = `Data Type`),
    fun.data = mean_sdl,
    fun.args = list(mult = 1),
    geom = "errorbar",
    width = 0.2,
    size = 1
  ) +
  # Mean points
  stat_summary(
    aes(color = Summary_Color, group = `Data Type`),
    fun = mean,
    geom = "point",
    size = 4
  ) +
  # Mean lines
  stat_summary(
    aes(color = Summary_Color, group = `Data Type`),
    fun = mean,
    geom = "line",
    size = 1
  ) +
  # Identity scale
  scale_color_identity(
    name = "Data Type", 
    breaks = c("#BF5B17", "#018571"), 
    labels = c("Imputed", "Unimputed"), 
    guide = "legend"
  ) +
  theme_bw(base_size = 18) +
  ylim(c(0, 1.05)) + 
  labs(x = "Total Samples per Class\n(before Splitting for FS [30%] and Train/Test [70%])", 
       y = "Validation Accuracy")
ggsave("Fig3_leduc.png", width = 10, height = 6, units = "in", dpi = 600)




