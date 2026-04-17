library(MSstats)
library(tidyverse)
library(data.table)
library(readxl)
source('plate_norm.R')


input = fread("Original_Data\\MarfanStudy_NewLibrary_all.tsv", sep="\t")

filename_map <- tibble(
  Run = input$File.Name
) %>%
  distinct() %>%
  mutate(Filename = str_extract(Run, "[^_]+$"))

annotation <- read_excel("Original_Data\\1-s2.0-S1535947626000459-mmc1.xlsx", sheet = "Table S4") %>%
  select(Filename, Batch, Sex, Genotype) %>%
  mutate(Condition = paste0(Genotype, "_", Sex)) %>%
  rename(BioReplicate = Batch) %>%
  left_join(filename_map) %>%
  select(Run, BioReplicate, Condition) %>%
  as.data.table()

annotation$Run = str_split_i(str_split_i(annotation$Run, "\\\\", i=5), "\\.", i=1)
input$File.Name = str_split_i(str_split_i(input$File.Name, "\\\\", i=5), "\\.", i=1)


## Manual DIANN converter
msstats_input = as.data.table(DIANNtoMSstatsFormat(input, annotation))
fwrite(msstats_input, file="Original_Data\\msstats_format.csv")


## Plate normalize
# msstats_input = fread(file="Original_Data\\msstats_format.csv")
msstats_input = msstats_input %>% filter(BioReplicate != "")

msstats_input$Plate = msstats_input$BioReplicate
msstats_input$Gender = unlist(str_split_i(msstats_input$BioReplicate, "\\_", i=1))

msstats_input[msstats_input$Intensity==0, "Intensity"] = NA
msstats_input$Intensity = log2(msstats_input$Intensity)


## Plate norm
msstats_input_norm = MSstatsPlateNormalize(msstats_input)

# Fix weird rep
msstats_input_norm[msstats_input_norm$BioReplicate == "F_WT_P1B", "BioReplicate"] = "F_WT_P1"

fwrite(msstats_input_norm, file="Original_Data\\msstats_norm_format_13.csv")
# msstats_input_norm = fread(file="Original_Data\\msstats_norm_format_13.csv")


## label cells with cell type
# input_diamter = fread(file="Original_Data\\msstats_norm_format_13.csv")

potential_biomarkers = c('PECA1_MOUSE','VWF_MOUSE','NOS3_MOUSE',
                         'CYGB_MOUSE', 'DPEP1_MOUSE',
                         'MYH11_MOUSE','TAGL_MOUSE','SMTN_MOUSE','CNN1_MOUSE',
                         'COR1A_MOUSE','C163A_MOUSE','CD14_MOUSE',
                         'UCP1_MOUSE')

# label smc and firbo cell types
msstats_input_norm_clustered = msstats_input_norm %>%
  group_by(Run) %>%
  mutate(Matched_Proteins = paste(unique(ProteinName[ProteinName %in% potential_biomarkers]), collapse=', ')) %>%
  ungroup()

# Use the biomarker proteins to assign it to a cluster.
msstats_input_norm_clustered$cluster = NA
msstats_input_norm_clustered <- msstats_input_norm_clustered %>%
  mutate(
    cluster = ifelse(grepl("SMTN_MOUSE", Matched_Proteins) &grepl("CNN1_MOUSE", Matched_Proteins), 
                     str_trim(paste(cluster, "smc", sep = ", ")), 
                     cluster),
    cluster = ifelse(grepl("DPEP1_MOUSE", Matched_Proteins) &grepl("CYGB_MOUSE", Matched_Proteins), 
                     str_trim(paste(cluster, "fibro", sep = ", ")), 
                     cluster),
  )


msstats_input_norm_clustered <- msstats_input_norm_clustered %>%
  mutate(cluster = str_replace_all(cluster, "\\bNA,\\s*", "")) %>%  # Remove "NA," at the beginning
  mutate(cluster = str_replace_all(cluster, "\\bNA\\b", "")) %>%    # Remove standalone "NA"
  mutate(cluster = str_trim(cluster))  

msstats_input_norm_clustered<- msstats_input_norm_clustered %>%
  mutate(cluster = ifelse(grepl("smc", cluster) & grepl("fibro", cluster), NA, cluster)) #get rid of proteins that classified as both fibro and smc

msstats_input_norm_clustered = msstats_input_norm_clustered %>% mutate(Condition = ifelse(is.na(cluster), as.character(Condition), paste(Condition, cluster, sep = "_")))

# print(head(msstats_input_norm_clustered))

msstats_input_norm_clustered %>% select(Run, cluster) %>% distinct() %>% group_by(cluster) %>% summarize(count = n()) %>% print()

fwrite(msstats_input_norm_clustered, file="Original_Data\\msstats_norm_clustered.csv")


## sumamrize the data
summarized = dataProcess(msstats_input_norm, featureSubset = "topN", 
                         n_top_feature=20, MBimpute = FALSE)
#  numberOfCores = 16)
save(summarized, file="Original_Data\\summarized_plate_norm_13.rda")
# load(file="Original_Data\\summarized_plate_norm_13.rda")

summarized$ProteinLevelData[
  summarized$ProteinLevelData$SUBJECT == "F_WT_P1B", 
  "SUBJECT"] = "F_WT_P1"

fwrite(summarized$ProteinLevelData, file="Original_Data\\msstats_norm_summarized.csv")

