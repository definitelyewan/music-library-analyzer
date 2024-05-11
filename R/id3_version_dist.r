
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  print("Please provide an artist")
  quit()
}


data_set <- read.csv(args[1], header = TRUE, sep = ",", quote = "")

version_1 <- data_set[grepl("Yes", data_set$ID3v1), ]
version_2 <- data_set[grepl("2", data_set$ID3v2_ver), ]
version_3 <- data_set[grepl("3", data_set$ID3v2_ver), ]
version_4 <- data_set[grepl("4", data_set$ID3v2_ver), ]

df <- data.frame(versions = c("ID3v1", "ID3v2.2", "ID3v2.3", "ID3v2.4"), occurances = c(nrow(version_1), nrow(version_2), nrow(version_3), nrow(version_4)))

write.table(df, row.names = FALSE, col.names = FALSE, sep = "|")