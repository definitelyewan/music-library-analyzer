options("width" = 200)

data_set <- read.csv("build/metadata.csv", header = TRUE, sep = ",", quote = "")

album <- data_set$Album
album_artists <- data_set$Album_Artist

df <- data.frame(artist = album_artists, album = album)

# Get unique rows
unique_df <- unique(df)

# Print the unique rows
print(unique_df)