from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import numpy as np
import time


def indirect_webdriver():
    options = webdriver.ChromeOptions()
    # for indirecting IP
    options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
    # for different UserAgent
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')

    # 다운로드 경로 지정
    download_dir = '/Users/shinbo/contest_repository/assembly/data/'
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir
    })

    driver = webdriver.Chrome()

    return driver

def indirect_request(url):

    ua = UserAgent()
    userAgent = ua.random
    fake_headers = {
        "User-Agent": userAgent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    r = requests.get(url, header=fake_headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup

def rand_time_sleep(min_val, max_val):
    rand_val = np.random.uniform(min_val, max_val)
    time.sleep(rand_val)
