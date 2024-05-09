library(ggplot2)
library(gridExtra)

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
