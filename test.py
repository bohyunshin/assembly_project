from bs4 import BeautifulSoup
import requests

url = 'https://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_K2F0C0Y5B2D2C1Z5B2F6T4S2K9N8V8'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

for a in soup.find('div', {'class':'links textType02 mt20'}).find_all('a'):
    print(a.text)