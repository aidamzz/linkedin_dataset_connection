from selenium import webdriver
from bs4 import BeautifulSoup
import os,random, sys, time
import sqlite3
from sqlite3 import Error

browser = webdriver.Chrome('D:/Algorithm/linkedin/LinkedIn-Auto-Connect-Bot-with-Personalized-Messaging/Driver/chromedriver.exe')
browser = webdriver.Chrome('D:/Algorithm/linkedin/LinkedIn-Auto-Connect-Bot-with-Personalized-Messaging/Driver/chromedriver.exe')

browser.get('https://www.linkedin.com/uas/login')

file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

fulllink = 'https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=v7S'

browser.get(fulllink)

def getNewProfileIDs(soup):
    profilesID = []
    pav = soup.find('div', {'class': 'ph0 pv2 artdeco-card mb2'})
    pav = pav.find('ul', {'class':'reusable-search__entity-result-list list-style-none'})
    all_links = pav.findAll('a', {'class': 'app-aware-link scale-down'})
    for link in all_links:

        userID = link.get('href')

        profilesID.append(userID)
    return profilesID

profilesID = getNewProfileIDs(BeautifulSoup(browser.page_source,features="html.parser"))

link = profilesID[2]



def get_info(link):
    browser.get(link)
    SCROLL_PAUSE_TIME = 5

    last_height = browser.execute_script("return document.body.scrollHeight")

    for i in range(3):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    scr = browser.page_source
    soup = BeautifulSoup(scr,features="html.parser")

    name_div = soup.find('div', {'class': 'mt2 relative'})
    name_loc = name_div.find_all('div')
    name = name_loc[0].find('h1').get_text().strip()
    print(name)
    location = soup.find('div', {'class':'pb2 pv-text-details__left-panel'})
    location = location.find('span', {'class':'text-body-small inline t-black--light break-words'}).get_text().strip()
    print(location)
    profile_title = name_loc[2].get_text().strip()
    print(profile_title)
    connection_ul = soup.find('ul', {'class':'pv-top-card--list pv-top-card--list-bullet display-flex pb1'})
    connection = connection_ul.find('span').get_text().strip()
    print(connection)

    exp_ul = soup.findAll('section',{'class':"artdeco-card ember-view relative break-words pb3 mt2"})
    if (exp_ul[2].find('span', {'visually-hidden'}).get_text().strip() == 'About') or (exp_ul[2].find('span', {'visually-hidden'}).get_text().strip() == 'Activity'):
        if exp_ul[1].find('span', {'visually-hidden'}).get_text().strip() == 'Featured':
            exp_div = exp_ul[4].findAll('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
        else:
            exp_div = exp_ul[3].findAll('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
    else:
        if exp_ul[1].find('span', {'visually-hidden'}).get_text().strip() == 'About':
            if exp_ul[2].find('span', {'visually-hidden'}).get_text().strip() == 'Featured':
                exp_div = exp_ul[4].findAll('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
            else:
                exp_div = exp_ul[2].findAll('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
        else:
            if exp_ul[1].find('span', {'visually-hidden'}).get_text().strip() == 'Activity':
                exp_div = exp_ul[2].findAll('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
            else:
                exp_div = exp_ul[1].findAll('li', {'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
    if exp_ul[1].find('span', {'visually-hidden'}).get_text().strip() == 'Education':
        edu_ul = exp_ul[1].findAll('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
        current_job_title = None
        company = None
        lenght_of = None
    else:
        current_job_title = exp_div[0].find('div', {'class': 'display-flex align-items-center'})
        current_job_title = current_job_title.find('span', {'class':'visually-hidden'}).get_text()
        print(current_job_title)
        company = exp_div[0].find('span', {'class':'t-14 t-normal'})
        company = company.find('span', {'class':'visually-hidden'}).get_text()
        print(company)
        lenght_of = exp_div[0].find('span', {'class': 't-14 t-normal t-black--light'})
        lenght_of = lenght_of.find('span', {'class':'visually-hidden'}).get_text()
        print(lenght_of)
        if (exp_ul[2].find('span', {'visually-hidden'}).get_text().strip() == 'About') or (exp_ul[2].find('span', {'visually-hidden'}).get_text().strip() == 'Activity'):
            if exp_ul[1].find('span', {'visually-hidden'}).get_text().strip() == 'Featured':

                edu_ul = exp_ul[5].findAll('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
            else:
                edu_ul = exp_ul[4].findAll('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
        else:
            if (exp_ul[1].find('span', {'visually-hidden'}).get_text().strip() == 'About')or (exp_ul[1].find('span', {'visually-hidden'}).get_text().strip() == 'Activity'):
                if exp_ul[2].find('span', {'visually-hidden'}).get_text().strip() == 'Featured':
                    edu_ul = exp_ul[5].findAll('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
                else:
                    edu_ul = exp_ul[3].findAll('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
            else:
                if exp_ul[1].find('span', {'visually-hidden'}).get_text().strip() == 'Activity':
                    edu_ul = exp_ul[3].findAll('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
            if exp_ul[0].find('span', {'visually-hidden'}).get_text().strip() == 'About':
                edu_ul = exp_ul[2].findAll('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
        if exp_ul[0].find('span', {'visually-hidden'}).get_text().strip() == 'Activity':
            edu_ul = exp_ul[2].findAll('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})

    last_education = edu_ul[0].find('div', {'class': 'display-flex align-items-center'})
    last_education_university = last_education.find('span', {'class':'visually-hidden'}).get_text()
    degree = edu_ul[0].find('span', {'class': 't-14 t-normal'})
    if degree != None:

        degree = degree.find('span', {'class':'visually-hidden'}).get_text()



    ro = (name,location,profile_title,connection,current_job_title,company,lenght_of,last_education_university,degree )

    return ro


conn = sqlite3.connect('linkedin.db')
c = conn.cursor()
c.execute("""CREATE TABLE Connections_info (
            user_name,
            user_location,
            profile_title,
            number_connections,
            current_job,
            company,
            time_in_current_company,
            last_education,
            degree
            )""")

for i in range(1, 95):
    fulllink = 'https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&page={}&sid=YSQ'.format(i)
    browser.get(fulllink)
    SCROLL_PAUSE_TIME = 5
    time.sleep(SCROLL_PAUSE_TIME)
    profilesID = getNewProfileIDs(BeautifulSoup(browser.page_source,features="html.parser"))
    while profilesID != []:
        user_link = profilesID.pop()
        l = get_info(user_link)
        query ="""INSERT INTO Connections_info (
                user_name,
                user_location,
                profile_title,
                number_connections,
                current_job,
                company,
                time_in_current_company,
                last_education,
                degree
                ) VALUES (?,?,?,?,?,?,?,?,?)"""
        c.execute(query,l)
        conn.commit()
conn.close()