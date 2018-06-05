

import os, sys
import csv
from bs4 import BeautifulSoup
import urllib2
import xlsxwriter
from selenium import webdriver
import pdb

reload(sys)
sys.setdefaultencoding('utf8')

###

key_stats_on_main =['Market Cap', 'PE Ratio (TTM)', 'EPS (TTM)']
key_stats_on_stat =['Enterprise Value', 'Trailing P/E', 'Forward P/E',
                     'PEG Ratio (5 yr expected)', 'Return on Assets', 'Quarterly Revenue Growth',
                     'EBITDA', 'Diluted EPS', 'Total Debt/Equity', 'Current Ratio']

stocks_arr =[]
pfolio_file= open("stocks.csv", "r")
for line in pfolio_file:
    indv_stock_arr = line.strip().split(',')
    stocks_arr.append(indv_stock_arr)

print(stocks_arr)

browser = webdriver.PhantomJS()
stock_info_arr = []

for stock in stocks_arr:
    stock_info = []
    ticker = stock[0]
    stock_info.append(ticker)

    url = "https://finance.yahoo.com/quote/{0}?p={0}".format(ticker)
    url2 = "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}".format(ticker)

    browser.get(url)
    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML, 'html.parser')
    for stat in key_stats_on_main:
        page_stat1 = soup.find(text=stat)
        try:
            page_row1 = page_stat1.find_parent('tr')
            try:
                page_statnum1 = page_row1.find_all('span')[1].contents[1].get_text(strip=True)
                print(page_statnum1)
            except:
                page_statnum1 = page_row1.find_all('td')[1].contents[0].get_text(strip=True)
                print(page_statnum1)
        except:
            print('Invalid parent for this element')
            page_statnum1 = "N/A"

        stock_info.append(page_statnum1)

    browser.get(url2)
    innerHTML2 = browser.execute_script("return document.body.innerHTML")
    soup2 = BeautifulSoup(innerHTML2, 'html.parser')
    for stat in key_stats_on_stat:
        page_stat2 = soup2.find(text=stat)
        try:
            page_row2 = page_stat2.find_parent('tr')
            try:
                page_statnum2 = page_row2.find_all('span')[1].contents[0].get_text(strip=True)
                print(page_statnum2)
            except:
                page_statnum2 = page_row2.find_all('td')[1].contents[0].get_text(strip=True)
                print(page_statnum2)
        except:
            print('Invalid parent for this element')
            page_statnum2 = 'N/A'
        stock_info.append(page_statnum2)

    stock_info_arr.append(stock_info)

print(stock_info_arr)

########## WRITING OUR RESULTS INTO EXCEL

key_stats_on_main.extend(key_stats_on_stat)
workbook = xlsxwriter.Workbook('Stocks01.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 1

for stat in key_stats_on_main:
    worksheet.write(row, col, stat)
    col +=1

row = 1
col = 0
for our_stock in stock_info_arr:
    col = 0
    for info_bit in our_stock:
        worksheet.write(row, col, info_bit)
        col += 1
    row += 1
workbook.close()

print('Script completed')
