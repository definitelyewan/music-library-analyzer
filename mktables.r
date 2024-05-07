#install.packages("ggplot2", repos='http://cran.us.r-project.org')
library(ggplot2)

id3v1_version_dist <- function(data_set) {
  version_1 <- data_set[grepl("Yes", data_set$ID3v1), ]
  version_2 <- data_set[grepl("2", data_set$ID3v2_ver), ]
  version_3 <- data_set[grepl("3", data_set$ID3v2_ver), ]
  version_4 <- data_set[grepl("4", data_set$ID3v2_ver), ]

  df <- data.frame(versions = c("ID3v1", "ID3v2.2", "ID3v2.3", "ID3v2.4"), occurances = c(nrow(version_1), nrow(version_2), nrow(version_3), nrow(version_4)))

  p <- ggplot(data = df, aes(x = versions, y = occurances, color = versions)) +
              geom_bar(stat = "identity", fill = "white") +
              geom_text(aes(label = occurances), vjust = 1.6, color = "black", size = 3.5) +
              theme(legend.position = "none") +
              ggtitle("ID3 Versions by Occurances")

  ggsave("output/id3v1_version_dist.png", plot = p, width = 6, height = 4, dpi = 300)

}

artist_count <- function(data_set){

  artist_counts <- strsplit(data_set$Artist, "/")
  artist_counts <- unlist(artist_counts)
  artist_counts <- trimws(artist_counts)
  artist_table <- table(artist_counts)
  artist_table <- sort(artist_table, decreasing = TRUE)

  df <- data.frame(artists = names(artist_table), counts = as.numeric(artist_table))

  print(df)
#   data <- data.frame(
#     group = LETTERS[1:5],
#     value = c(13,7,9,21,2)
#   )

#   # Basic piechart
#   ggplot(data, aes(x="", y = value, fill = group)) +
#     geom_bar(stat = "identity", width = 1, color = "white") +
#     coord_polar("y", start = 0) +
#     theme_void() # remove background, grid, numeric labels


    # artist_table <- sort(artist_table, decreasing = TRUE)
    # other_artists <- sum(artist_table[-(1:30)])
    # artist_table <- c(artist_table[1:30], Other = other_artists)

    # pie3D(artist_table, main="Percentage of Artist Contributions", col=rainbow(length(artist_table)))
    # legend("bottom", 
    #        legend=paste(names(artist_table[1:30]), 
    #        "(", round(artist_table[1:30]/sum(artist_table)*100, 2), "%)"), 
    #        fill=rainbow(length(artist_table)),
    #        horiz = TRUE)
#     #barplot(artist_table, main="Artist Counts", xlab="Artist", ylab="Count", horiz=FALSE, names.arg=names(artist_table), las=1)


}


setwd(".")

data <- read.csv("build/metadata.csv", header = TRUE, sep = ",", quote = "")

id3v1_version_dist(data)

artist_count(data)
