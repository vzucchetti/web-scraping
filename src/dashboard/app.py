import streamlit as st
import pandas as pd
import sqlite3

#connecting with SQLite
conn = sqlite3.connect('../data/quotes.db')

#loading data from database table in a dataframe using a SQL query
df = pd.read_sql_query('SELECT * FROM mercadolivre_itens', conn)

#closing connection to database
conn.close()

#title of application
st.title('Market Research - Sport Shoes on Mercado Livre')

#subtitle
st.subheader('Main KPIs')
#improving layout dividing the number of columns and defining which you KPI want to occupy in order
col1,col2,col3 = st.columns(3)

#creating KPI for show in application
#KPI 1 - total number of itens; '.shape' do a count of itens
total_itens = df.shape[0]
col1.metric(label='Total Number of Itens', value=total_itens)

#KPI 2 - number of unique brands
unique_brands = df['brand'].nunique()
col2.metric(label='Number of Unique Brands', value=unique_brands)

#KPI 3 - average of price considering the new price (in reais)
average_new_price = df['new_price'].mean()
col3.metric(label='Average New Price (R$)', value=f'{average_new_price:.2f}')

#Which brands are mostly found until the last page
st.subheader("Brands Mostly Found")
col1, col2 = st.columns([4,2]) #indicate proportions for each column
top_brands = df['brand'].value_counts().sort_values(ascending=False)
col2.write(top_brands)
top_brands.index = pd.CategoricalIndex(top_brands.index, categories=top_brands.index, ordered=True) #ordering the index to present chart in desending order
col1.bar_chart(top_brands)

#Which is the average price by brand
st.subheader('Brands Average Price')
col1, col2 = st.columns([4,2])
df_non_zero_prices = df[df['new_price'] > 0]
average_price_bybrand = df_non_zero_prices.groupby('brand')['new_price'].mean().sort_values(ascending=False).round(2)
col2.write(average_price_bybrand.rename('average price (R$)'))
average_price_bybrand.index = pd.CategoricalIndex(average_price_bybrand.index, categories=average_price_bybrand.index, ordered=True)
col1.bar_chart(average_price_bybrand)

#Which is the satisfaction by brand
st.subheader('Brands Satisfaction')
col1, col2 = st.columns([4,2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False).round(2)
col2.write(satisfaction_brand.rename('satisfaction'))
satisfaction_brand.index = pd.CategoricalIndex(satisfaction_brand.index, categories=satisfaction_brand.index, ordered=True)
col1.bar_chart(satisfaction_brand)