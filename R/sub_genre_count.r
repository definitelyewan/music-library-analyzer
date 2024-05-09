data_set <- read.csv("build/metadata.csv", header = TRUE, sep = ",", quote = "")

genres <- data_set$Genre

genres <- strsplit(genres, "/")
genres <- unlist(genres)
genres <- tolower(genres)

# special considerations

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

df <- data.frame(genres = names(genre_table), frequency = as.numeric(genre_table))

print(df)
