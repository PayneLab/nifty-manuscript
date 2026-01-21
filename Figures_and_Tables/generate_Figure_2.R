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



# plot hard dataset
ggplot(data = montalvo_imputed_data, mapping = aes(x = `Samples per Class`, y = `Validation Accuracy`)) + 
  geom_jitter(position = position_jitter(width = 0.2), alpha = 0.3, color = "red", size = 2) + 
  stat_summary(fun.data = "mean_sdl", # Calculates mean and standard deviation
               fun.args = list(mult = 1), # For 1 standard deviation
               geom = "errorbar", # Draws the error bars
               width = 0.2, 
               size = 1) + # Adjust the width of the error bars
  stat_summary(fun = "mean", # Calculates the mean
               geom = "point", # Draws a point at the mean
               size = 4, # Adjust the size of the point
               color = "black") + # Set the color of the mean point
  # Add a line connecting the means
  stat_summary(fun = "mean",
               geom = "line",
               aes(group = 1), # Ensures a single line is drawn across all categories
               color = "black", 
               size = 1) +
  theme_bw(base_size = 18) + 
  ylim(c(0, 1.05)) + 
  labs(x = "Total Samples per Class\n(before Splitting for FS [30%] and Train/Test [70%])", y = "Validation Accuracy", title = "Imputed Dataset")
ggsave("Fig2_montalvo_imputed.png", width = 8, height = 6, units = "in", dpi = 600)



ggplot(data = montalvo_unimputed_data, mapping = aes(x = `Samples per Class`, y = `Validation Accuracy`)) + 
  geom_jitter(position = position_jitter(width = 0.2), alpha = 0.3, color = "red", size = 2) + 
  stat_summary(fun.data = "mean_sdl", # Calculates mean and standard deviation
               fun.args = list(mult = 1), # For 1 standard deviation
               geom = "errorbar", # Draws the error bars
               width = 0.2, 
               size = 1) + # Adjust the width of the error bars
  stat_summary(fun = "mean", # Calculates the mean
               geom = "point", # Draws a point at the mean
               size = 4, # Adjust the size of the point
               color = "black") + # Set the color of the mean point
  # Add a line connecting the means
  stat_summary(fun = "mean",
               geom = "line",
               aes(group = 1), # Ensures a single line is drawn across all categories
               color = "black", 
               size = 1) +
  theme_bw(base_size = 18) + 
  ylim(c(0, 1.05)) + 
  labs(x = "Total Samples per Class\n(before Splitting for FS [30%] and Train/Test [70%])", y = "Validation Accuracy", title = "Original Dataset")
ggsave("Fig2_montalvo_original.png", width = 8, height = 6, units = "in", dpi = 600)



# plot easy dataset
ggplot(data = leduc_imputed_data, mapping = aes(x = `Samples per Class`, y = `Validation Accuracy`)) + 
  geom_jitter(position = position_jitter(width = 0.2), alpha = 0.3, color = "red", size = 2) + 
  stat_summary(fun.data = "mean_sdl", # Calculates mean and standard deviation
               fun.args = list(mult = 1), # For 1 standard deviation
               geom = "errorbar", # Draws the error bars
               width = 0.2, 
               size = 1) + # Adjust the width of the error bars
  stat_summary(fun = "mean", # Calculates the mean
               geom = "point", # Draws a point at the mean
               size = 4, # Adjust the size of the point
               color = "black") + # Set the color of the mean point
  # Add a line connecting the means
  stat_summary(fun = "mean",
               geom = "line",
               aes(group = 1), # Ensures a single line is drawn across all categories
               color = "black", 
               size = 1) +
  theme_bw(base_size = 18) + 
  ylim(c(0, 1.05)) + 
  labs(x = "Total Samples per Class\n(before Splitting for FS [30%] and Train/Test [70%])", y = "Validation Accuracy", title = "Imputed Dataset")
ggsave("Fig2_leduc_imputed.png", width = 8, height = 6, units = "in", dpi = 600)



ggplot(data = leduc_unimputed_data, mapping = aes(x = `Samples per Class`, y = `Validation Accuracy`)) + 
  geom_jitter(position = position_jitter(width = 0.2), alpha = 0.3, color = "red", size = 2) + 
  stat_summary(fun.data = "mean_sdl", # Calculates mean and standard deviation
               fun.args = list(mult = 1), # For 1 standard deviation
               geom = "errorbar", # Draws the error bars
               width = 0.2, 
               size = 1) + # Adjust the width of the error bars
  stat_summary(fun = "mean", # Calculates the mean
               geom = "point", # Draws a point at the mean
               size = 4, # Adjust the size of the point
               color = "black") + # Set the color of the mean point
  # Add a line connecting the means
  stat_summary(fun = "mean",
               geom = "line",
               aes(group = 1), # Ensures a single line is drawn across all categories
               color = "black", 
               size = 1) +
  theme_bw(base_size = 18) + 
  ylim(c(0, 1.05)) + 
  labs(x = "Total Samples per Class\n(before Splitting for FS [30%] and Train/Test [70%])", y = "Validation Accuracy", title = "Original Dataset")
ggsave("Fig2_leduc_original.png", width = 8, height = 6, units = "in", dpi = 600)




