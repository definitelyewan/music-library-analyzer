args <- commandArgs(trailingOnly = TRUE)
options("width" = 201)

if (length(args) == 0) {
  print("Please provide an artist")
  quit()
}

search_artist <- tolower(args[1])
search_artist <- gsub(",", "", search_artist)

data_set <- read.csv("build/metadata.csv", header = TRUE, sep = ",", quote = "")
data_set[sapply(data_set, is.character)] <- lapply(data_set[sapply(data_set, is.character)], tolower)
data_set <- data_set[apply(data_set, 1, function(x) any(grepl(search_artist, x))), ]

print(paste0("Search query: ", search_artist))

# contributed works
album_table <- table(data_set$Album)
album_df <- data.frame(album = names(album_table), songs = as.numeric(album_table))
print(paste0("Contributed to ",nrow(album_df), " projects between ", min(data_set$Year), " - ", max(data_set$Year)))

print(album_df)


print(paste0("Total songs: ", sum(as.numeric(album_df$songs))))

title_df <- data.frame(title = gsub("/", ",",data_set$Title), from_album = data_set$Album, year = data_set$Year)
print(title_df)


#attributed genres

genres <- data_set$Genre

genres <- strsplit(genres, "/")
genres <- unlist(genres)
genres <- tolower(genres)

genres <- gsub("nu\\s", "nu-", genres)
genres <- gsub("neo\\s", "neo-", genres)
genres <- gsub("free\\s", "free-", genres)
genres <- gsub("alt\\s", "alt-", genres)
genres <- gsub("post\\s", "post-", genres)
genres <- gsub("big\\s", "big-", genres)
genres <- gsub("hard\\s", "hard-", genres)
genres <- gsub("new\\s", "new-", genres)
genres <- gsub("art\\s", "art-", genres)
genres <- gsub("art\\s", "art-", genres)
genres <- gsub("\\sand\\s", "-and-", genres)
genres <- gsub("heavy\\s", "heavy-", genres)
genres <- gsub("\\shop", "-hop", genres)
genres <- gsub("abstract\\s", "abstract-", genres)
genres <- gsub("prog\\s", "prog-", genres)

genres <- gsub("bossa nova", "bossa-nova", genres)
genres <- gsub("boom bap", "boom-bap", genres)
genres <- gsub("cloud rap", "cloud-rap", genres)
genres <- gsub("black metal", "black-metal", genres)
genres <- gsub("east coast", "east-coast", genres)
genres <- gsub("west coast", "west-coast", genres)
genres <- gsub("video game", "video-game", genres)
genres <- gsub("spoken word", "spoken-word", genres)
genres <- gsub("hiphop", "hip-hop", genres)

genres <- strsplit(genres, " ")
genres <- unlist(genres)

genres <- genres[genres != ""]
genres <- genres[genres != " "]


genres <- trimws(genres)
genres <- tolower(genres)
genre_table <- table(genres)
genre_table <- sort(genre_table, decreasing = TRUE)

print(paste0("Works in ", length(genre_table), " genres :"))
df <- data.frame(genres = names(genre_table), songs = as.numeric(genre_table))
print(df)

max_genre <- max(as.numeric(genre_table))
genre_name <- names(genre_table)[as.numeric(genre_table) == max_genre]



