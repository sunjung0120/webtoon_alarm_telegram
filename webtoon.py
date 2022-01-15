import requests #웹 크롤링에 필요한 모듈들 설치
from bs4 import BeautifulSoup
import time
import telegram
from apscheduler.schedulers.blocking import BlockingScheduler

bot = telegram.Bot(token='5092297175:AAHm9oHm885i0uoct7IzwfohqHmLl4w3V_k')

#_____________________________
#텔레그램 봇 토큰을 위함. 이 부분 수정하기

url = 'https://comic.naver.com/webtoon/weekday' 

def job_fuction(): #계속 체크해 줘야 하므로
    html = requests.get(url) 
    soup = BeautifulSoup(html.text,'html.parser') #html.parser = html의 규칙에 맞게 해석해라.

    page = 1
        
    up = soup.select_one('em.ico_updt') #em 클래스에 있는 ico_updt = up체크

    now = time.localtime()

    try :
        while True :
            if(up) : 
                up_2 = up.find_parent('div',class_='col_inner') #이렇게 해서, 부모 클래스를 찾을 수 있다.
                title = up_2.select_one('div > ul > li:nth-child({0}) > a'.format(page)).text.strip() #제목 만들때 사용했던것 그대로 넣어주기, 대신 div.info-movie 안에 있는
                if now.tm_hour == 00 and now.tm_min == 00 and now.tm_sec == 00 : #00시가 되면 웹툰이 자동으로 올라오므로, 체크하지 않습니다.
                    break

                bot.sendMessage(chat_id='5036633660', text = '"' + title + '" '+'웹툰이 업로드 되었습니다.')
                page += 1
                sched.pause() #이렇게 하면, 한번 메세지가 오면 멈출 수 있다.

    except : #마지막 페이지를 체크하는 방법이 오류밖에 없는 것 같아서, 일단
        print("마지막 페이지 입니다.")

sched = BlockingScheduler()
sched.add_job(job_fuction, 'interval', seconds = 3) #interval이라는 것을 이용해서, 일정간격마다 반복하겠다는 의미로
sched.start()