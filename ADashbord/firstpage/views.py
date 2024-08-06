from django.shortcuts import render
from . import sentmint_analysis
import pandas as pd
import numpy as np

# Create your views here.

def index(request):

    # load data frame
    df, df_TIME_OF_TWEET = sentmint_analysis.see_data()

    # convert data frame to html
    #
    data = [
                (time, count, percentage)
                for time, count, percentage in zip(
                    np.round(df_TIME_OF_TWEET['Percentage'].to_list(),2),
                    df_TIME_OF_TWEET['Count'].to_list(),
                    df_TIME_OF_TWEET['Time of Tweet'].to_list())
                ]

    df_age_group = sentmint_analysis.Age_group()

    data_age_group = [
                (age_group, count, percentage)
                for age_group, count, percentage in zip(
                    np.round(df_age_group['Percentage'].to_list(),2),
                    df_age_group['Count'].to_list(),
                    df_age_group['Age group'].to_list())
                ]
    df_sentiment = sentmint_analysis.sentiment()

    data_sentiment = [
                (sentiment, count, percentage)
                for sentiment, count, percentage in zip(
                    np.round(df_sentiment['Percentage'].to_list(),2),
                    df_sentiment['Count'].to_list(),
                    df_sentiment['Sentiment'].to_list())
                ]
    df_avg = sentmint_analysis.active_user()

    bar_plot = sentmint_analysis.bar_plot()

    histo = sentmint_analysis.histogram()


    number = 5
    if request.method =='POST':
        number = int(request.POST.get('rows'))
        if number > 10:
            number = 10
        elif number < 1:
            number = 1
        else:
            number = number

    train_data = sentmint_analysis.train_data(number)

    train_data_zip = [
                (text, selected_text, sentiment)
                for text, selected_text, sentiment in zip(
                    train_data['text'].to_list(),
                    train_data['selected_text'].to_list(),
                    train_data['sentiment'].to_list())
                ]




    context = {
        'data': data,
        'df': df,
        'total_count' : df['Time of Tweet'].count(),
        'age_group' : data_age_group,
        'total_count_age_group' : df['Age of User'].count(),
        'sentiment' : data_sentiment,
        'total_count_sentiment' : df['sentiment'].count(),
        'data_avg': df_avg,
        'bar_plot': bar_plot,
        'sentiment_percentage': np.round(df_sentiment['Percentage'].to_list(),2),
        'histo': histo,
        'train_data': train_data_zip,
        'number': number,

    }


    return render(request, 'pages/index.html', context=context)





def data(request):
    df, df_time_if_tweet = sentmint_analysis.see_data()
    x = pd.DataFrame(df.head(100))
    df_html = x.to_html(classes='table table-striped table-hover',index=False, justify='center')

    return render(request, 'pages/data.html', {'df': df,'df_html':df_html })
