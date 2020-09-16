import yfinance as yf
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import os

pd.set_option("display.max_rows", None, "display.max_columns", None)

company_name = input("Enter a company name: ")
root = "https://finance.yahoo.com"
link = "https://finance.yahoo.com/quote/" + str(company_name)

#get company max history and write to file
ti = yf.Ticker(company_name)
company_history = ti.history("max")
del company_history["Dividends"]
del company_history["Stock Splits"]
#print(type(company_history))
company_history = company_history.iloc[::-1]
#calculate attitude Close now and Close 3 days ago
company_history['3day_before_change'] = company_history['Close'] / company_history['Close'].shift(-3)
dir = "./companies/" + str(company_name) + "/"
filename = dir + str(company_name) + ".csv"
os.makedirs(os.path.dirname(filename), exist_ok=True)
f = open(filename, "w+")
f.write(str(company_history))

#get news about a company and write to file
req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
with requests.Session() as C:
    soup = BeautifulSoup(webpage, 'html.parser')
    list = []
    for item in soup.find_all('div', attrs={'class': 'Py(14px) Pos(r)'}):
        news_link = str(item.find('a', href=True)['href'])
        news_title = str(item.find('h3', attrs={'class': 'Mb(5px)'}).get_text())
        list.append(news_title + "\t" + (root + news_link) + "\n")
        #print(news_link)
        #print(news_title)

news = dir + "News.csv"
f = open(news, "w+")
for item in list:
    f.write(item)