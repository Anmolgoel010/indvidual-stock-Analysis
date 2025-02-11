import pandas as pd 
import numpy as np 
import datetime as dt 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import cufflinks as cf 
import plotly.io as pio
import plotly.graph_objects as go
cf.go_online()
pio.renderers.default = 'browser'

stock_df = pd.read_csv('WMT.csv')  #reading the csv file
#print(stock_df.info())

#Creating a new column for daily return
stock_df['Daily Return'] = stock_df['Adj Close'].pct_change(1) * 100      
print(stock_df.describe().round(2))  #description of each column

#Creating a line graph showing the closing adjusted price of the stock over time
fig = px.line(title = 'Walmart.com, Inc. (WMT) Adjusted Closing Price [$]')
fig.add_scatter(x = stock_df['Date'], y = stock_df['Adj Close'], name = 'Adj Close')

def plot_financial_data(df, title):
    fig = px.line(title = title, animation_frame='Date', color_discrete_sequence=['#1f77b4'])
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'], y = df[i], name = i)
        fig.update_traces(line_width = 5)
        fig.update_layout({'plot_bgcolor': "white",  'title_font_size':16})
fig.show()  #shows the line graph of the ajdusted closing price


#defining a function that classifies the daily return
def percentage_return_classifier(percentage_return):
    if percentage_return > -0.3 and percentage_return <= 0.3:
        return 'Insignificant Change'
    elif percentage_return > 0.3 and percentage_return <= 3:
        return 'Positive Change'
    elif percentage_return > -3 and percentage_return <= -0.3:
        return 'Negative Change'
    elif percentage_return > 3 and percentage_return <= 7:
        return 'Large Positive Change'
    elif percentage_return > -7 and percentage_return <= -3:
        return 'Large Negative Change'
    elif percentage_return > 7:
        return 'Bull Run'
    elif percentage_return <= -7:
        return 'Bear Sell Off'

#Creating a new column "trend" that classifies the daily return
stock_df['Trend'] = stock_df['Daily Return'].apply(percentage_return_classifier)
print(stock_df) 
trend_summary = stock_df['Trend'].value_counts()
print(trend_summary)

#Pie chart of the trend summary
fig = px.pie(names=trend_summary.index, values=trend_summary.values, 
             title="Walmart Daily Return Trend",
             color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']) 
fig.update_layout(title_font_size=16)
fig.show()


#Candlestick chart
cds = go.Figure(data=[go.Candlestick(x=stock_df['Date'],
                open=stock_df['Open'],
                high=stock_df['High'],
                low=stock_df['Low'],
                close=stock_df['Close'],
                increasing_line_color='#1f77b4',
                decreasing_line_color='#d62728', showlegend=True, increasing_line_width=4, decreasing_line_width=4,whiskerwidth=0.2)])
cds.update_layout(title="Walmart Candlestick Chart", plot_bgcolor="white", title_font_size=16, xaxis_rangeslider_visible=False, xaxis=dict(type='category', tickangle=45), yaxis=dict(autorange=True, fixedrange=False))
cds.show()


#scatterplot showing the relationship between the trading volume and the closing price
plt.figure(figsize = (10, 8))
sns.scatterplot(x = stock_df['Volume'], y = stock_df['Adj Close'], hue = stock_df['Trend'], palette = 'coolwarm',  color='#1f77b4', alpha=0.7)
plt.title('Walmart.com, Inc. (WMT) Volume[in million $] vs. Adj Close', fontsize=14, fontweight='bold')
plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
plt.show()