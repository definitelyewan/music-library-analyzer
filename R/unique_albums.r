
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  print("Please provide an artist")
  quit()
}

data_set <- read.csv(args[1], header = TRUE, sep = ",", quote = "")

album <- data_set$Album
album_artists <- data_set$Album_Artist

df <- data.frame(artist = album_artists, album = album)

unique_df <- unique(df)
sorted_df <- unique_df[order(unique_df$artist, unique_df$album), ]

write.table(sorted_df, row.names = FALSE, col.names = FALSE, sep = "|")