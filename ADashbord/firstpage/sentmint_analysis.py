import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib, base64

def see_data():
    df = pd.read_csv('/Users/abhisingh/Dashbord/ADashbord/archive/train.csv', encoding='latin-1')

    # uniquw count of tweets time
    unique_count_TTIME_OF_TWEET = df['Time of Tweet'].value_counts().to_dict()

    # sorting the dictionary
    unique_count_TTIME_OF_TWEET = dict(sorted(unique_count_TTIME_OF_TWEET.items(), key=lambda item: item[1], reverse=True))

    # calculating the percentage of each time of tweet

    percentage = [(i / df['Time of Tweet'].count()) * 100 for i in unique_count_TTIME_OF_TWEET.values() ]

    # creating a new data frame
    df_TIME_OF_TWEET = pd.DataFrame({'Time of Tweet': list(unique_count_TTIME_OF_TWEET.keys()), 'Count': list(unique_count_TTIME_OF_TWEET.values()), 'Percentage': percentage})
    return df, df_TIME_OF_TWEET

def Age_group():

    df = pd.read_csv('/Users/abhisingh/Dashbord/ADashbord/archive/train.csv', encoding='latin-1')
    # uniquw count of tweets time
    unique_count_Age_group = df['Age of User'].value_counts().to_dict()

    # sorting the dictionary
    unique_count_Age_group = dict(sorted(unique_count_Age_group.items(), key=lambda item: item[1], reverse=True))

    # calculating the percentage of each time of tweet

    percentage = [(i / df['Age of User'].count()) * 100 for i in unique_count_Age_group.values() ]

    # creating a new data frame
    df_Age_group = pd.DataFrame({'Age group': list(unique_count_Age_group.keys()), 'Count': list(unique_count_Age_group.values()), 'Percentage': percentage})

    return df_Age_group

def sentiment():
    df = pd.read_csv('/Users/abhisingh/Dashbord/ADashbord/archive/train.csv', encoding='latin-1')

    # uniquw count of tweets time
    unique_count_sentiment = df['sentiment'].value_counts().to_dict()

    # sorting the dictionary
    unique_count_sentiment = dict(sorted(unique_count_sentiment.items(), key=lambda item: item[1], reverse=True))

    # calculating the percentage of each time of tweet

    percentage = [(i / df['sentiment'].count()) * 100 for i in unique_count_sentiment.values() ]

    # creating a new data frame
    df_sentiment = pd.DataFrame({'Sentiment': list(unique_count_sentiment.keys()), 'Count': list(unique_count_sentiment.values()), 'Percentage': percentage})

    return df_sentiment


def active_user():

    df = pd.read_csv('/Users/abhisingh/Dashbord/ADashbord/archive/train.csv', encoding='latin-1')

    # uses some potential information
    country_count = len(df['Country'].unique())

    total_population_avg = df['Population -2020'].agg('mean')

    total_land_area_avg = df['Land Area (Km²)'].agg('mean')

    total_population_density_avg = df['Density (P/Km²)'].agg('mean')

    data = {
        'Country_Count': country_count,
        'Total_Population_Avg': total_population_avg,
        'Total_Land_Area_Avg': total_land_area_avg,
        'Total_Population_Density_Avg': total_population_density_avg,

    }

    return data

# set one time for all graph
def setgraph():
    buffer = io.BytesIO()# create a buffer to hold the plot
    plt.savefig(buffer, format='png')# save the plot to the buffer
    buffer.seek(0)# set the pointer to the start of the file
    image_png = buffer.getvalue()# get the content of the buffer
    graph = base64.b64encode(image_png)# encode the content to base64
    graph = graph.decode('utf-8')# convert to utf-8
    buffer.close()# close the buffer
    return graph # return the base64 encoded image

def bar_plot():
    df = pd.read_csv('/Users/abhisingh/Dashbord/ADashbord/archive/train.csv', encoding='latin-1')

    # group by age of user
    grouped_data = df.groupby(['sentiment', 'Time of Tweet']).agg({
        'Age of User' : 'count'
    }).reset_index()

    # plot the graph

    plt.switch_backend('AGG')# change the backend to AGG
    plt.figure(figsize=(10,5))# set the size of the plot
    plt.title('comparison of sentiment and time of tweet and count of age group')
    sns.barplot(y='Age of User', x='Time of Tweet',hue='sentiment', data=grouped_data)
    plt.xticks(rotation=45)# rotate the x-axis labels
    plt.legend(loc='upper left')# set the legend to the upper right
    plt.tight_layout()# adjust the plot to prevent clipping

    graph = setgraph()
    return graph

def histogram():

    df = pd.read_csv('/Users/abhisingh/Dashbord/ADashbord/archive/train.csv', encoding='latin-1')

    # plot the graph
    grouped_data = df.groupby(['sentiment', 'Country']).agg({
        'Age of User' : 'count'
    })

    p = grouped_data.loc['positive'][100:120].reset_index()
    n = grouped_data.loc['negative'][100:120].reset_index()
    nu = grouped_data.loc['neutral'][100:120].reset_index()

    mearge_data_frame = pd.merge(p,n,on='Country',how='outer')
    final_Data = pd.merge(mearge_data_frame,nu,on='Country',how='outer')

    plt.switch_backend('AGG')# change the backend to AGG
    plt.figure(figsize=(12,6))# set the size of the plot
    plt.title('comparison of sentiment and country and count of age group')# set the title of the plot
    sns.barplot(data=final_Data,x='Country',y='Age of User_x',hue='Age of User')
    sns.barplot(data=final_Data,x='Country',y='Age of User_y')
    plt.xticks(rotation=60)# rotate the x-axis labels
    plt.ylabel('Sentiment count', color='blue',fontsize=30)# set the label of the y-axis
    plt.legend(loc='upper left')# set the legend to the upper right
    plt.tight_layout()# adjust the plot to prevent clipping

    graph = setgraph()

    return graph

def train_data(number):
    df = pd.read_csv('/Users/abhisingh/Dashbord/ADashbord/archive/train.csv', encoding='latin-1')
    text = df['text'][:number]
    selectd_text = df['selected_text'][:10]
    sentiment = df['sentiment'][:10]

    data = {
        'text': text,
        'selected_text': selectd_text,
        'sentiment': sentiment

    }

    return data
