library(tidyverse)
library(lubridate)

greecegang <- read.csv("/Users/mbp/Documents/Side-Projects/iMessage_Analysis/greecegang_senti.csv")
messages <- read.csv("/Users/mbp/Documents/Side-Projects/iMessage_Analysis/imessage_data.csv")

# Explore the data:
head(greecegang)

# Fix column formats:
greecegang$date = as.Date(greecegang$date)
greecegang$text = as.character(greecegang$text)
greecegang$timestamp = ymd_hms(greecegang$timestamp,tz=Sys.timezone())
greecegang$name = as.character(greecegang$name)

# monthly number of texts for each person:
greecegang %>%
  mutate(month = format(date, "%m")) %>%
  group_by(month, name) %>% tally() %>%
  ggplot(aes(x = month, y = n, color = name)) + 
  geom_col(aes(fill= name)) + facet_wrap(~name, ncol = 2) +
  labs(title = "Number of Messages per Month", subtitle = "By Person: From 5/11/19 - 9/8/20",
       x = "Month", y = "Number of Messages") + theme_minimal() + 
  theme(legend.position = 'bottom', legend.title = element_blank())
ggsave("Plots/grouptexts_byperson.png", width = 8, height = 5)

# greecegang %>% filter(year == 2020) %>% 
#   mutate(month = format(date, "%m")) %>%
#   group_by(month) %>% tally() %>%
#   ggplot(aes(x = month, y = n)) + 
#   geom_col()


# average texts per day:
avg_perday = sum(!is.na(greecegang$text))/length(unique(greecegang$date))

# 7 day moving average for all combined:
mov_avg_all = greecegang %>% group_by(date) %>% tally() %>% mutate(mov_avg_all= zoo::rollmean(x = n, k = 7, fill = NA))

# Plot 7-day moving averages for each person:
greecegang %>% group_by(date, name) %>% tally() %>% group_by(name) %>%
  mutate(mov_avg = zoo::rollmean(x = n, k = 7, fill = NA)) %>%
  ggplot(aes(x = date, y = mov_avg, color = name)) + geom_line(alpha = 0.5, size = 1.1) +
  geom_vline(xintercept = as.Date("2020-03-17"), color = 'red') +
  annotate(
    geom = 'text',
    x = as.Date('2020-03-05'),
    y = 30,
    label = 'COVID SHUTDOWN 3/17',
    hjust = 1,
    size = 3,
    family = 'Helvetica'
  ) +
  labs(
    title = "Group Daily Texts",
    subtitle = "7-Day Moving Average",
    x = NULL,
    y = NULL
  ) +
  scale_x_date(
    date_breaks = "4 months",
    date_minor_breaks = "1 month",
    date_labels = "%B '%y",
    limits = as.Date(c("2019-05-11", "2020-09-08"))
  ) + 
  theme_minimal() +
  theme(legend.position = 'bottom', legend.title = element_blank(),
        axis.line = element_line())
ggsave("Plots/grouptexts_dailytexts.png", width = 8, height = 5)

# Sentiment analysis:

# Distribution of sentiment scores:
greecegang %>% ggplot(., aes(x = sentiment)) + 
  geom_density(fill = 'red', alpha = 0.6) + 
  labs(title = "Distribution of Sentiment Scores - Group Chat",
       x = "Sentiment Score",
       y = "Density") + 
       theme_minimal()
ggsave("Plots/sentiment_density.png")

# Average sentiment score per month:
greecegang %>%
mutate(month = format(date, "%m")) %>%
group_by(month) %>% summarise(mean_sent = mean(sentiment)) %>%
ggplot(aes(x = month, y = mean_sent)) + geom_col(position = "dodge", fill = "blue", alpha = 0.3) + 
labs(title = "Monthly Average Sentiment Scores",
      x = "Month",
      y = "Average Sentiment Score") + theme_minimal()
ggsave("Plots/sentiment_monthly.png", width = 8, height = 5)
       
  