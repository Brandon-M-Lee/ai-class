import os
import datetime
os.system('pip3 install -r requirements.txt')
import FinanceDataReader as fdr
import pandas as pd
import matplotlib.pyplot as plt

cnt=0

def get_data(date, code):
    date = datetime.datetime.strptime(date, '%Y.%m.%d.')
    data = fdr.DataReader(code, date)
    return data

def get_delta(date, data):
    date = datetime.datetime.strptime(date, '%Y.%m.%d.')
    date = datetime.datetime.strftime(date, '%Y-%m-%d')
    return data.loc[date]['Close'] - data.loc[date]['Open']

with open('article_data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        company, date, code = line.strip().split('\t')
        data = get_data(date, code)
        delta = get_delta(date, data)
        print(delta)
        if delta > 0:
            cnt+=1

print(cnt/444)