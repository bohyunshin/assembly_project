from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import shutil
import sqlite3
import numpy as np

from .indirect_crawl_test import indirect_request, indirect_webdriver, rand_time_sleep

def setFromTo(FromNum, ToNum):
    From = driver.find_elements_by_xpath(f"//option[@value='{str(FromNum)}']")[0]
    To = driver.find_elements_by_xpath(f"//option[@value='{str(ToNum)}']")[1]

    From.click()
    To.click()

def setProposer(ProposerName):
    search = driver.find_element_by_xpath('//*[@id="srchForm"]/div/div[3]/input[1]')
    search.send_keys(ProposerName)
    # driver.find_element_by_name('proposer').send_keys(ProposerName)

def search():
    xpath_SearchBox = '//*[@id="srchForm"]/div/div[6]/button[1]'
    driver.find_element_by_xpath(xpath_SearchBox).click()

def pageOption(pageNum):
    page = driver.find_element_by_xpath(f"//option[@value='{str(pageNum)}']")
    page.click()

def updateOneRow(db, vals_list):
    db_conn = sqlite3.connect(db, isolation_level=None)
    c = db_conn.cursor()

    c.execute("""
                INSERT INTO 
                assembly(
                billNum, 
                billName,
                billId,
                proposerCategory,
                proposerData,
                decisionDate,
                decisionResult,
                mainProposer,
                subProposer) 
                VALUES(?,?,?,?,?,?,?,?,?)
                """, vals_list)
download_dir = '/Users/shinbo/contest_repository/assembly/data/'

driver = indirect_webdriver()
driver.get('https://likms.assembly.go.kr/bill/main.do')

# 국회 시작 및 만료 기간 지정
# FromAge = input()
# ToAge = input()
setFromTo(20, 20)
# 검색 버튼 클릭
search()
# 페이지당 결과 수를 100으로 지정
pageOptionNum = 10
pageOption(pageOptionNum)

billNum = []
billName = []
billId = []
proposerCategory = []
proposerDate = []
decisionDate = []
decisionResult = []

mainProposer = []
subProposer = []

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
soup_tbody = soup.find('table',
        {'summary':'검색결과의 의안번호, 의안명, 제안자구분, 제안일자, 의결일자, 의결결과, 주요내용, 심사진행상태 정보'}).find('tbody')

for tr in soup_tbody.find_all('tr'):
    for idx,td in enumerate(tr.find_all('td')):

        # 의안번호
        if idx == 0:
            billNum.append(td.text)
        # 의안명
        elif idx == 1:
            billName.append(td.find('a').get('title'))
        # 제안자구분
        elif idx == 2:
            proposerCategory.append(td.text)
        # 제안일자
        elif idx == 3:
            proposerDate.append(td.text)
        # 의결일자
        elif idx == 4:
            decisionDate.append(td.text)
        # 의결결과
        elif idx == 5:
            decisionResult.append(td.text)



for i in range(1,pageOptionNum+1):

    # 파일을 다운로드할 디렉토리를 만든다
    try:
        os.mkdir(download_dir + str(billNum[i-1]))
    except:
        pass

    # 의안별 XML Path 지정
    xmlPath = f'/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{i}]/td[2]/div[2]/a'
    # 각 의안 페이지로 들어가기
    driver.find_element_by_xpath(xmlPath).click()

    time.sleep(np.random.uniform(5, 10))

    # 대표발의자 뽑아내기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    main_ = soup.find('table', {'summary':'의안접수정보의 의안번호, 제안일자, 제안자, 문서, 제안회기 정보'}).find_all('td')[2].text.strip()
    mainProposer.append(main_)

    # billId 뽑아내기
    billId_startIndex = driver.current_url.find('=') + 1
    Current_billId = driver.current_url[billId_startIndex:]
    billId.append(Current_billId)

    # 공동제안자 뽑아내기
    Coactor_URL = f'https://likms.assembly.go.kr/bill/coactorListPopup.do?billId={Current_billId}'

    # Open a new window
    driver.execute_script("window.open('');")
    # Switch to the new window and open URL B
    driver.switch_to.window(driver.window_handles[1])
    driver.get(Coactor_URL)

    # 공동 제안자 parsing
    Coactor_html = driver.page_source
    soup_Coactor = BeautifulSoup(Coactor_html, 'html.parser')
    Coactor_tags = soup_Coactor.find('div', {'class':'links textType02 mt20'})

    Coactor_list = []
    # 공동발의자가 없는 경우
    if Coactor_tags is None:
        pass
    else:
        for a_tag in Coactor_tags.find_all('a'):
            Coactor_list.append(a_tag.text)
    # close Coactor url
    driver.close()
    # switch to original tab
    driver.switch_to.window(driver.window_handles[0])

    # 공동발의자 추가하기
    subProposer.append(' '.join(Coactor_list))

    time.sleep(np.random.uniform(5, 10))

    # # 제안자 뽑아내기
    # proposer_Xpath = "//img[@src='/bill/images/sub/btn_pp01.gif']/.."
    #
    # # 공동 제안자 목록이 없을 경우를 대비
    # try:
    #     driver.find_element_by_xpath(proposer_Xpath).click()
    #     print(driver.page_source)
    #
    #     time.sleep(10)
    # except:
    #     pass

    # pdf의 xpath: pdf 아이콘이 있는 xpath의 부모 노드
    # 우선 모든 pdf를 다운 받는다
    pdf_Xpath_list = driver.find_elements_by_xpath("//img[@src='/bill/images/icon/icon_pdf.png']/..")
    for path in pdf_Xpath_list:
        path.click()
        time.sleep(np.random.uniform(10, 15))

    # 다운로드한 파일을 의안번호 폴더에 옮긴다
    files = [ file for file in os.listdir(download_dir) \
              if os.path.isfile(os.path.join(download_dir, file))]

    for file in files:
        shutil.move(download_dir + file,
                    download_dir + str(billNum[i-1]) + '/' + file)

    # 목록으로 되돌아가기 (뒤로가기)
    xmlPath_listBtn = "//div[@class='listBtn']/a"
    driver.find_element_by_xpath(xmlPath_listBtn).click()

    time.sleep(np.random.uniform(3,6))

# database에 업데이트
for i in range(len(billNum)):
    updateOneRow('../db/assembly.db',
                 [billNum[i],
                 billName[i],
                 billId[i],
                 proposerCategory[i],
                 proposerDate[i],
                 decisionDate[i],
                 decisionResult[i],
                 mainProposer[i],
                 subProposer[i]])

driver.quit()


