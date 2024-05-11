args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  print("Please provide an artist")
  quit()
}


data_set <- read.csv(args[1], header = TRUE, sep = ",", quote = "")

feat_titles <- data_set$Title[grepl("((\\(|\\[)feat.*|(\\(|\\[)ft.*)", data_set$Title, ignore.case = TRUE)]
feat_titles <- gsub("^.*(\\(|\\[)(feat|ft)(\\. | )", "", feat_titles, ignore.case = TRUE)
feat_titles <- gsub("(\\)|\\]).*$", "", feat_titles, ignore.case = TRUE)
feat_titles <- strsplit(feat_titles, "/")
feat_titles <- unlist(feat_titles)
feat_titles <- strsplit(feat_titles, ";")
feat_titles <- unlist(feat_titles)
feat_titles <- trimws(feat_titles)

artist_counts <- strsplit(data_set$Artist, "/")
artist_counts <- unlist(artist_counts)
artist_counts <- strsplit(artist_counts, ";")
artist_counts <- unlist(artist_counts)
artist_counts <- trimws(artist_counts)
artist_counts <- c(artist_counts, feat_titles)


artist_table <- table(artist_counts)
artist_table <- sort(artist_table, decreasing = TRUE)

total_counts <- length(artist_table)
percentages <- (as.numeric(artist_table) / total_counts) * 100
df <- data.frame(artists = names(artist_table), percentage = round(percentages, 2), frequency = as.numeric(artist_table))
df <- df[order(df$artists, decreasing = FALSE), ]

write.table(df, row.names = FALSE, col.names = FALSE, sep = "|")
