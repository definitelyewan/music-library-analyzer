

if (!require(ggplot2)) {
  install.packages("ggplot2", repos = "http://cran.us.r-project.org")
}

if (!require(gridExtra)) {
  install.packages("gridExtra", repos = "http://cran.us.r-project.org")
}

library(ggplot2)
library(gridExtra)

id3v1_version_dist <- function(data_set) {
  version_1 <- data_set[grepl("Yes", data_set$ID3v1), ]
  version_2 <- data_set[grepl("2", data_set$ID3v2_ver), ]
  version_3 <- data_set[grepl("3", data_set$ID3v2_ver), ]
  version_4 <- data_set[grepl("4", data_set$ID3v2_ver), ]

  df <- data.frame(versions = c("ID3v1", "ID3v2.2", "ID3v2.3", "ID3v2.4"), occurances = c(nrow(version_1), nrow(version_2), nrow(version_3), nrow(version_4)))
  print("What version of ID3 has the most occurances?")
  print(df)

#   p <- ggplot(data = df, aes(x = versions, y = occurances, color = versions)) +
#               geom_bar(stat = "identity", fill = "white") +
#               geom_text(aes(label = occurances), vjust = 1.6, color = "black", size = 3.5) +
#               theme(legend.position = "none") +
#               ggtitle("ID3 Versions by Occurances")

#   ggsave("output/id3v1_version_dist.png", plot = p, width = 6, height = 4, dpi = 300)

}

artist_count <- function(data_set) {

  feat_titles <- data_set$Title[grepl("((\\(|\\[)feat.*|(\\(|\\[)ft.*)", data_set$Title, ignore.case = TRUE)]
  feat_titles <- gsub("^.*(\\(|\\[)(feat|ft)(\\. | )", "", feat_titles, ignore.case = TRUE)
  feat_titles <- gsub("(\\)|\\]).*$", "", feat_titles, ignore.case = TRUE)
  feat_titles <- strsplit(feat_titles, "/")
  feat_titles <- unlist(feat_titles)
  feat_titles <- strsplit(feat_titles, "&")
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
  df <- data.frame(artists = names(artist_table), percentage = round(percentages, 2), counts = as.numeric(artist_table))
  
  print("What artist contributed the most to your library?")
  print(df)
#   df <- df[order(-df$percentage_of_library), ]
#   num_rows <- nrow(df)
#   png_height <- 20 * num_rows


#   png("output/artist_count.png", width = 620, height = png_height)
#   grid.table(df)
#   invisible(dev.off())
}

album_count <- function(data_set) {

  print(unique(data_set$Album))


#   df <- data.frame(artists = names(artist_table), albums = as.numeric(artist_table))
#   print(df)
#   df <- df[order(-df$as.numeric(artist_table)), ]
#   num_rows <- nrow(df)
#   png_height <- 20 * num_rows

#   png("output/artist_projects.png", width = 620, height = png_height)
#   grid.table(df)
#   invisible(dev.off())
}

setwd(".")
options("width" = 200)
data <- read.csv("build/metadata.csv", header = TRUE, sep = ",", quote = "")

id3v1_version_dist(data)
artist_count(data)

#album_count(data)
