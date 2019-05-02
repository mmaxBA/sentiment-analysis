import boto3
import json

def sentiment(text):
    comprehend = boto3.client(service_name='comprehend',
                                region_name='us-east-2')
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='es')#["Sentiment"]
    if(sentiment["Sentiment"] == "NEUTRAL"):
        if(sentiment["SentimentScore"]["Positive"]>sentiment["SentimentScore"]["Negative"]):
            return "POSITIVE"
        else:
            return "NEGATIVE"
    sentiment["Sentiment"]
