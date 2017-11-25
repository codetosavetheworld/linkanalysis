import networkx as nx
G=nx.barabasi_albert_graph(60,41)
pr=nx.pagerank(G,0.4)
pr

# Before executing below code install BeautifulSoup and schedule, run this statement on Anaconda - pip install <>

import schedule
import time
import requests
from BeautifulSoup import BeautifulSoup

url = "http://www.google.com"   # replace this url 
response = requests.get(url)
# parse html
page = str(BeautifulSoup(response.content))

#creates schedules
def job():

    def getURL(page):
    """

    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """
        start_link = page.find("a href")
        if start_link == -1:
            return None, 0
            start_quote = page.find('"', start_link)
            end_quote = page.find('"', start_quote + 1)
            url = page[start_quote + 1: end_quote]
            return url, end_quote

    while True:
        url, n = getURL(page)
        page = page[n:]
        if url:
            print url
            else:
                break

schedule.every(1).minutes.do(job) # you can choose an scheduler ou want of your choice
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
