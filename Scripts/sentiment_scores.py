# Sentiment Analysis

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Instantiate analyzer:
analyzer = SentimentIntensityAnalyzer()

# Load Group Chat DataFrame:
greece_gang = pd.read_csv("/Users/mbp/Documents/Side-Projects/iMessage_Analysis/greece_gang.csv")

# Calculate sentiment scores for each text in group chat:
greece_gang['text'] = greece_gang.text.astype(str)
scores = []
for texts in greece_gang.text:
    tokens = word_tokenize(texts)
    tokens_clean = [word for word in tokens if not word in stopwords.words('english')]
    tokens_sentence = (" ").join(tokens_clean)
    score = analyzer.polarity_scores(tokens_sentence)
    scores.append(score)

compound_scores = []
for i in range(0,len(scores)):
    compound_scores.append(scores[i]['compound'])

# add scores to dataframe:
greece_gang['sentiment'] = compound_scores

# Write to csv for further analysis:
greece_gang.to_csv('/Users/mbp/Documents/Side-Projects/iMessage_Analysis/greecegang_senti.csv')
