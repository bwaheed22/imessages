## Analyzing iMessage Data
## Script to pull and clean message data, save to CSV:
##

# Import packages:
import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
%matplotlib inline

conn = sqlite3.connect('/Users/mbp/Documents/Side-Projects/iMessage_Analysis/chat.db') # connect to db
cur = conn.cursor() # create cursor object to query db using sql syntax

# get the names of the tables in the database
cur.execute(" select name from sqlite_master where type = 'table' ")
for name in cur.fetchall():
    print(name)

## Prepare data from relevant tables:

messages = pd.read_sql_query('''select *, datetime(date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime")  as date_utc from message''', conn)

handles = pd.read_sql_query("select * from handle", conn)
chat_message_joins = pd.read_sql_query("select * from chat_message_join", conn)

messages['message_date'] = messages['date']
messages['timestamp'] = messages['date_utc'].apply(lambda x: pd.Timestamp(x))
messages['date'] = messages['timestamp'].apply(lambda x: x.date())
messages['month'] = messages['timestamp'].apply(lambda x: int(x.month))
messages['year'] = messages['timestamp'].apply(lambda x: int(x.year))


# rename the ROWID into message_id, because that's what it is
messages.rename(columns={'ROWID' : 'message_id'}, inplace = True)

# rename appropriately the handle and apple_id/phone_number as well
handles.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)

# merge the messages with the handles
merge_level_1 = pd.merge(messages[['text', 'handle_id', 'date','message_date' ,'timestamp', 'month','year','is_sent', 'message_id']],  handles[['handle_id', 'phone_number']], on ='handle_id', how='left')

# and then that table with the chats
df_messages = pd.merge(merge_level_1, chat_message_joins[['chat_id', 'message_id']], on = 'message_id', how='left')


## Write to CSV

# Save data for future use:
df_messages.to_csv('/Users/mbp/Documents/Side-Projects/iMessage_Analysis/imessage_data.csv', index = False, encoding = 'utf-8')

## ------ Simple Data exploration: -------
df_messages['date'].min(), df_messages['date'].max()


# number of messages per day
plt.plot(df_messages[df_messages['year']==2018].groupby('date').size())
plt.xticks(rotation='45')

plt.bar(x=sorted(df_messages.month.unique()), height = df_messages.groupby('month').size())

# number of messages per month and year
df_messages.groupby('month').size()
df_messages.groupby('year').size()

# how many messages sent versus received
df_messages.groupby('is_sent').size()

## ---- Extract Group Chat Data for Group Chat Analysls: -----

# Extract group chat:
greece_gang = df_messages[df_messages['chat_id']==242]

greece_gang.shape

greece_gang['date'].min(), greece_gang['date'].max()

# Match phone numbers to names. Eli had multiple phone numbers and email adresses.
# I will use his current number as his main, and others as "eli other". I also had an "nan" which I will label
# as myself (Bilal).
name_lookup = pd.DataFrame({'phone_number': greece_gang.phone_number.unique(),
'name': ['Dan', 'Bilal', 'Christopher', 'Eli', 'Bilal', 'Eli', 'Eli']})

# Merge names to group chat dataframe:
greece_gang = greece_gang.merge(name_lookup, how='left', on = 'phone_number')
greece_gang.head()

# Clean up data frame to only include columns of interest:
greece_gang = greece_gang[['text','date','year','timestamp','name']]

# Write group chat to csv for further analysis:
greece_gang.to_csv('/Users/mbp/Documents/Side-Projects/iMessage_Analysis/greece_gang.csv')
