
ID3v1_contents_pie_graph <- function(data_set) {
    yes_values <- data_set[grepl("Yes", data_set$ID3v1), ]
    no_values <- data_set[grepl("No", data_set$ID3v1), ]

    labels <- c("Contains ID3v1", "No ID3v1")
    sizes <- c((nrow(yes_values) / nrow(data_set)) * 100, (nrow(no_values) / nrow(data_set)) * 100)
    sizes <- round(sizes, 2)
    colors <- c("blue", "green")

    pie(sizes, labels=sizes, col=colors, main="Files with ID3v1 tags")
    legend("bottom", legend=labels, fill=colors, xpd=TRUE, inset=c(0, -0.3))
}

ID3v2_versions_pie_graph <- function(data_set) {
    version_2 = data_set[grepl("2", data_set$ID3v2_ver), ]
    version_3 = data_set[grepl("3", data_set$ID3v2_ver), ]
    version_4 = data_set[grepl("4", data_set$ID3v2_ver), ]

    labels <- c("Percentage of ID3v2.2", "Percentage of ID3v2.3", "Percentage of ID3v2.4")
    sizes <- c((nrow(version_2) / nrow(data_set)) * 100, 
               (nrow(version_3) / nrow(data_set)) * 100,
               (nrow(version_4) / nrow(data_set)) * 100)
    sizes <- round(sizes, 2)
    colors <- c("blue", "green", "red")
    pie(sizes, labels=sizes, col=colors, main="ID3v2 Version Distribution")
    legend("bottom", legend=labels, fill=colors, xpd=TRUE, inset=c(0, -0.3))

}

artist_count_graph <- function(data_set){
    
    artist_counts <- strsplit(data_set$Artist, "/")
    artist_counts <- unlist(artist_counts)
    artist_counts <- trimws(artist_counts)

    artist_table <- table(artist_counts)
    pie(artist_table, main="Artist Counts", labels=names(artist_table), col=rainbow(length(artist_table)))
    #barplot(artist_table, main="Artist Counts", xlab="Artist", ylab="Count", horiz=FALSE, names.arg=names(artist_table), las=1)


}


setwd(".")
par(mfrow = c(2, 2))
data <- read.csv("build/metadata.csv", header=TRUE, sep=",", quote="")

ID3v1_contents_pie_graph(data)
ID3v2_versions_pie_graph(data)
par(mfrow = c(1, 1))
artist_count_graph(data)

