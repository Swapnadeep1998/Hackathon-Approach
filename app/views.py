# import tensorflow as tf
from django.shortcuts import render
from tensorflow.keras.models import load_model
from rest_framework import viewsets
from django.core import serializers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from . import models
from .serializers import SentimentSerializers
import pandas as pd
import numpy as np
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# Create your views here.
def register(request):
    return render(request, 'sentiment/register.html')


def login(request):
    return render(request, 'sentiment/login.html')

# Real Project


class sentimentviews(viewsets.ModelViewSet):
    queryset = models.Sentiment.objects.all()
    serializer_class = SentimentSerializers


@api_view(['POST'])
def sentimentclassifier(request):
    try:
        max_length = 100
        trunc_type = 'post'
        mydata=request.data
        model=load_model('./app/model/sentiment.h5')

        with open('./app/model/tokenizer.json') as f:
            data = json.load(f)
            tokenizer = tokenizer_from_json(data)

        test_sequence = tokenizer.texts_to_sequences(list(mydata.values()))
        test_padded = pad_sequences(test_sequence , maxlen = max_length, padding= 'post', truncating= trunc_type)
        result = model.predict(test_padded)
        result=(result>=0.5)
        new_df=pd.DataFrame(result,columns=['Status'])
        new_df=new_df.replace({True:'Positive',False:'Negative'})

        return Response(new_df)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
