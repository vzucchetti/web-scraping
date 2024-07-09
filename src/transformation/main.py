import pandas as pd
import sqlite3
from datetime import datetime

#opening the JSONL file with data collected and returnin a dataframe
df = pd.read_json('../data/data.jsonl', lines=True)

#setting pandas to show all columns
pd.options.display.max_columns = None

#adding columns to the dataframe
df['_source'] = 'https://lista.mercadolivre.com.br/tenis-corrida-masculino' #columns to indicate here the data came from

df['_collect_date'] = datetime.now() #indicate the date and time of the collect

#transforming null values in 0
#values are all as string in JSON; transforming the numeric values from string to float
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_cents'] = df['old_price_cents'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_cents'] = df['new_price_cents'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

#removing parenthesis from column 'review_amount'
#'replace' command used to replace parenthesis for nothing
#'/' indicates anything, so this '[\(\)]' means, preserve anything until and between the parenthesis, removing only the parenthesis
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
#transforming null values in 0 and from string to int
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

#combinating the main price and cents in a unique value
df['old_price'] = df['old_price_reais'] + df['old_price_cents']/100 #division to convert the value to cent (0.01)
df['new_price'] = df['new_price_reais'] + df['new_price_cents']/100

#removing the older columns of price
df.drop(columns=['old_price_reais','old_price_cents','new_price_reais','new_price_cents'], inplace=True)

#connecting to SQLite database
conn = sqlite3.connect('../data/quotes.db')

#saving the dataframe in the SQLite
#'if_exists' indicates that is the database already exists, replace by the new one
#'index=False' indicates to not save in the database the line numbers
df.to_sql('mercadolivre_itens', conn, if_exists='replace', index=False)

#closing connection with database
conn.close()

#show the result dataframe
print(df.head())