data_set <- read.csv("build/metadata.csv", header = TRUE, sep = ",", quote = "")

year_frequency <- table(data_set$Year)

year_frequency <- sort(year_frequency, decreasing = TRUE)
total_counts <- length(data_set$Year)
percentages <- (as.numeric(year_frequency) / total_counts) * 100

df <- data.frame(year = as.numeric(names(year_frequency)), frequency = as.numeric(year_frequency), percentage = round(percentages, 2))

print(df)