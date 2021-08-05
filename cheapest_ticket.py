#Программа, которая ищет самый дешевый билет в самый телпый город России


import requests
from bs4 import BeautifulSoup
import re
from itertools import groupby
from functools import reduce
import datetime
import datetime as DT
from operator import add
import pandas as pd
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
resp = requests.get('https://www.gismeteo.ru/', headers=headers)
html = resp.text
soup = BeautifulSoup(html,'html.parser')

def get_links():
    links = []
    for i in soup.find_all('noscript', {'id':'noscript'}):
        f = re.findall(r'/weather-[a-z]+-[0-9]+', str(i))
        links.append(f)
    links = list(set(sum(links, [])))
    all_links = []
    for k in links:
        all_links.append('https://www.gismeteo.ru' + k +'/10-days')
    return all_links

def load_forecast(link:str) -> list:
    resp = requests.get(link, headers=headers)
    html = resp.text
    soup = BeautifulSoup(html,'html.parser')
    date = []
    for i in soup.find_all('div', {'class' :'w_date'}):
        f = re.findall(r'\d+\s[а-я]*', str(i))
        date.append(f)
    date = list(set(sum(date, [])))
    date = [line.strip() for line in date]
    date_2 = []
    for i in date:
        q = ''.join(h for h in i if not h.isalpha())
        q = q.replace(' ','')
        date_2.append(q)
    datetime_date = []
    now = datetime.date.today()
    all_date = []
    for k in date_2:
        if int(k) >= int((now.strftime("%d"))):
            all_date.append(now.strftime("%Y%m") + str(k))
        else:
            all_date.append(now.strftime("%Y") + str(int(now.strftime("%m")) + 1) + str(k))
    for k in all_date:
        date = DT.datetime.strptime(k, '%Y%m%d').date()
        datetime_date.append(date)
    datetime_date = sorted(datetime_date)
    sorteddates = [datetime.datetime.strftime(j, "%Y-%m-%d") for j in datetime_date]
    for i in soup.find_all('div', {'class' :'subnav_search_city js_citytitle'}):
        city = re.findall(r'[А-Я][а-я]*', str(i))
    summary = []
    for i in soup.find_all('span', {'class' :'tooltip'}):
        summ = re.findall(r'[А-Я].*[а-я]*.{1}[а-я]+[а-я]+', str(i))
        summary.append(summ)
    summary = sum(summary, [])
    all_temp = []
    for i in soup.find_all('div', {'class' :'value'}):
        k = re.findall(r'[−+]{0,1}\d{1,2}',str(i))
        if len(k) == 7:
            all_temp.append(k[3])
            all_temp.append(k[5])
        elif len(k) == 5:
            all_temp.append(k[3])
            all_temp.append(k[3])
    new_temp = []
    for l in all_temp:
        if l.startswith('−'):
            x = l.replace('−','')
            x = int(x)
            new_temp.append(-(x))
        else:
            new_temp.append(int(l))
    max_temp = new_temp[0::2]
    min_temp = new_temp[1::2]
    max_wind_speed = []
    for i in soup.find_all('span', {'class' :'unit unit_wind_m_s'}):
        speed = re.findall(r'\d{1,2}',str(i))
        max_wind_speed.append(speed)
    max_wind_speed = sum(max_wind_speed,[])[:10]
    precipitation = []
    for i in soup.find_all('div', {'class' :'w_prec__value'}):
        speed = re.findall(r'\d[,]?\d?',str(i))
        if len(speed) == 1:
            precipitation.append(speed[0])
        else:
            precipitation.append(speed[-1])
    if len(precipitation) == 0:
        l = 0
        while l != 10:
            precipitation.append('0')
            l += 1
    pressure = []
    for i in soup.find_all('div', {'class' :'value'}):
        press = re.findall(r'[7]\d{2}',str(i))
        if press != []:
            pressure.append(press)
    for j, k in enumerate(pressure):
        if len(k) == 1:
            k.append(k[0])
            pressure[j] == k
    max_pressure = sum(pressure[0::2],[])[:10]
    min_pressure = sum(pressure[1::2],[])[:10]
    end = []
    for k in range(len(date_2)):
        d = {'date':sorteddates[k],
             'city':city[0],
             'summary':summary[k],
             'max_temp':max_temp[k],
             'min_temp':min_temp[k],
             'max_wind_speed':max_wind_speed[k],
             'precipitation':float(precipitation[k].replace(',','.')),
             'max_pressure':max_pressure[k],
             'min_pressure':min_pressure[k]}
        end.append(d)
    return end

def load_all_forecasts():
    links = get_links()
    all_cities = []
    for k in links:
        city = load_forecast(k)
        all_cities.append(city)
    return all_cities

forecasts = sum(load_all_forecasts(), [])

df = pd.DataFrame(forecasts)
df['date'] = pd.to_datetime(df['date'])
df['max_temp_rolling'] = df['max_temp'].rolling(window=3).mean()
df['day_of_week'] = None
for i,j in enumerate(df['date']):
    df['day_of_week'][i] = j.weekday()

def find_best_city(df):
    average ={}
    cities = [el for el, _ in groupby(df['city'].values)]
    for city in cities:
        one_city = df[lambda x: x['city'] == city]
        temp_6 = one_city[lambda x: x['day_of_week'] == 6]
        temp_5 = one_city[lambda x: x['day_of_week'] == 5]
        if one_city['day_of_week'].values[0] != 6:
            max_temp_6 = temp_6['max_temp'].values[0]
            max_temp_5 = temp_5['max_temp'].values[0]
            min_temp_6 = temp_6['min_temp'].values[0]
            min_temp_5 = temp_5['min_temp'].values[0]
            average_temp = (max_temp_5 + max_temp_6 + min_temp_5 + min_temp_6)/4
            average[city] = average_temp
            date = temp_5[temp_5.day_of_week == 5]['date'].values[0]
        else:
            max_temp_6 = temp_6['max_temp'].values[1]
            max_temp_5 = temp_5['max_temp'].values[0]
            min_temp_6 = temp_6['min_temp'].values[1]
            min_temp_5 = temp_5['min_temp'].values[0]
            average_temp = (max_temp_5 + max_temp_6 + min_temp_5 + min_temp_6)/4
            average[city] = average_temp
            date = temp_5[temp_5.day_of_week == 5]['date'].values[0]
    for k, v in average.items():
        if v == max(average.values()):
            return k,date

def find_cheapest_ticket(best_city: str, depart_date) -> dict :
    date =  datetime.datetime.utcfromtimestamp(depart_date.tolist()/1e9)
    date = (date).strftime('%Y-%m-%d')
    page= 'http://min-prices.aviasales.ru/calendar_preload'
    link = 'http://autocomplete.travelpayouts.com/places2?term={}&locale=ru&types[]=city'.format(best_city)
    best_city_iata = requests.get(link).json()[0]['code']
    req = requests.get(page, headers=headers, params = {'origin': 'MOW',
    'destination': best_city_iata,
    'depart_date': date,
    'one_way': 'true'}).text
    y = json.loads(req)
    new = []
    best_prices = y.get('best_prices')
    for k in best_prices:
        for j, v in k.items():
            if j == 'value':
                new.append(v)
    prices = {}
    l = str(min(new))
    if len(new) != 0:
        prices['price'] = min(new)
    else:
        prices['error'] = 'Билетов нет'
    return prices
cheapest_price = find_cheapest_ticket(find_best_city(df)[0],find_best_city(df)[1])

def main_fuction():
    for j, b in cheapest_price.items():
        if j == 'price':
            return 'You better go to ' + find_best_city(df)[0] + '.' + ' The price is ' + str(b)
        else:
            return 'You better stay home'
print(main_fuction())