from django.shortcuts import render
from . import sentmint_analysis
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from .models import Sentiment

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






@login_required
def loginuser(request):
    if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                # Authenticate and log in the user
                user = form.get_user()
                login(request, user)
                return redirect('/')  # Redirect to a success page or dashboard
            else:
                # Handle form errors
                messages.error(request, 'Invalid username or password')
                return render(request, 'login.html', {
                        'form': form,
                        'msg': messages.get_messages(request)
                    })
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form, 'msg': messages.get_messages(request)})

@login_required
def logout_user(request):

    return render(request, 'accounts/login.html')
@login_required
def password_reset(request):

    return render(request, 'accounts/password_reset.html')
@login_required
def register(request):

    return render(request, 'accounts/register.html')


def sentiment(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        context = data(text)

        # context and text should add in model.py
        sentiment = Sentiment(given_text=text, sentiment_score=context['score'], sentiment=context['result'])
        sentiment.save()

        return render(request, 'pages/data.html', context=context)
    return render(request, 'pages/data.html')

def data(text):
    # preapeare the model

    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"  # Example sentiment model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    # encode the text
    result = tokenizer.encode(text, return_tensors="pt",truncation=True,padding=True)
    result = model(result)
    result =int(torch.argmax( result.logits))+1

    score = result

    if result == 1 or result == 2:
        result = "Negative"
    elif result == 3:
        result = "Neutral"
    else:
        result = "Positive"

    context = {
        'text': text,
        'result': result,
        'score': score
    }

    return context
