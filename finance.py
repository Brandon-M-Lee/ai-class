import os
import datetime
os.system('pip3 install -r requirements.txt')
import FinanceDataReader as fdr
import pandas as pd
import matplotlib.pyplot as plt

def get_data(date, code):
    date = datetime.datetime.strptime(date, '%Y.%m.%d.')
    delta = datetime.timedelta(days=10)
    data = fdr.DataReader(code, date - delta, date + delta)
    data['High'].plot()

get_data('2022.04.11.', '005301')