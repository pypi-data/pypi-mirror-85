from parser_libraries import functions as f
from bs4 import BeautifulSoup
import os
import logging
import logging.handlers

host = 'http://www.arbitr.ru'
url = host+'/as/'
addition = 'about/ourJudges/'
addition_kr = 'kasyanova'


logging.basicConfig(format=f'%(module)s.{__name__}: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def parser_person(link, wbsite):
    try:
        html = f.get_html(link["link"])
        soup = BeautifulSoup(html.text, 'html.parser')
        soup = soup.find('div', class_='b-content-body js-content-body')
        try:
            image_link = wbsite[:-1] + soup.find('img').get('src')
        except:
            image_link = '-'
        name = soup.find('div', class_='b-card-title-container')
        work = name.find('h3', class_='b-card-title b-card-post').get_text().lower()
        name = name.find('h2').get_text().replace('.', ' ')
        if name == "" or name == None:
            name = link["name"].replace(".", " ")
        name = f.get_name(name)
        date = soup.find_all('dl', class_='b-card-info-block g-clrfix')
        try:
            date = date[-1].get_text().lower()
            if date.find('родился') != -1:
                year = date.find('года')
                if year != -1:
                    date = date[date.find('родился')+len('родился'):year]
                elif date.find('г.') != -1:
                    date = date[date.find('родился')+len('родился'):date.find('г.')]
            elif date.find('родилась') != -1:
                year = date.find('года')
                if year != -1:
                    date = date[date.find('родилась') + len('родилась'):year]
                elif date.find('г.') != -1:
                    date = date[date.find('родилась') + len('родилась'):date.find('г.')]
            else:
                date = date[date.find('.')-2:date.find('.')+8]
            date = date.replace('.', ' ')
            date = f.get_dig_date(date)
        except:
            date = -1
        lst = {}
        if date == -1 or date['year'] > 2000:
            lst = {
            'image_link': image_link,
            'first_name': name[1],
            'middle_name': name[2],
            'last_name': name[0],
            'link': link["link"],
            'bday': 1,
            'bmonth': 1,
            'byear': 1901,
            'position_id': f.get_work(work, 42),
            }
        else:
            lst = {
            'image_link': image_link,
            'first_name': name[1],
            'middle_name': name[2],
            'last_name': name[0],
            'link': link["link"],
            'bday': date['day'],
            'bmonth': date['month'],
            'byear': date['year'],
            'position_id': f.get_work(work, 42),
            }
        return lst
    except:
        return 1


def parser_people_links(link):
    links = []
    if link.find('krasnoyarsk') != -1:
        html = f.get_html(link+addition+addition_kr)
    else:
        html = f.get_html(link + addition)
    soup = BeautifulSoup(html.text, 'html.parser')
    soup = soup.find('div', class_='l-columns')
    if soup != None:
        soup = soup.find('div', class_='l-column l-column--left js-column')
        try:
            soup1 = soup.find('ul', class_='b-menu js-menu menu')
            soup1 = soup1.find('li', class_='b-menu-item js-menu-item b-menu-item--active js-menu-item--active b-menu-item--is_submenu')
            soup1 = soup1.find('div', class_='b-submenu js-submenu b-submenu--all')
            soup1 = soup1.find('ul', class_='b-menu js-menu menu')
            soup1 = soup1.find_all('li')
        except:
            try:
                soup3 = soup.find_all('ul', class_='b-menu js-menu menu accordion')
                soup3 = soup3[3]
                soup1 = soup3.find_all('li')
            except:
                try:
                    soup2 = soup.find('ul', class_='b-menu js-menu menu accordion')
                    soup2 = soup2.find('li', class_='b-menu-item js-menu-item b-menu-item--active js-menu-item--active b-menu-item--is_submenu')
                    soup2 = soup2.find('div', class_='b-submenu js-submenu b-submenu--accordion')
                    soup2 = soup2.find('ul', class_='b-menu js-menu menu accordion')
                    soup1 = soup2.find_all('li')
                except:
                    soup3 = soup.find('ul', class_='b-menu js-menu menu ')
                    soup3 = soup3.find('li', class_= 'b-menu-item js-menu-item b-menu-item--active js-menu-item--active b-menu-item--is_submenu first')
                    soup3 = soup3.find('div', class_='b-submenu js-submenu b-submenu--all')
                    soup3 = soup3.find('ul', class_='b-menu js-menu menu ')
                    soup1 = soup3.find_all('li')
        for sou in soup1:
            sou = sou.find('a', class_='item_link')
            if sou != None:
                links.append({"link":link[:-1] + sou.get('href'), "name": sou.get_text()})
    else:
        links = None
    return links


def parser_direct_link(link):
    html = f.get_html(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    soup = soup.find_all('table', cellpadding='5')
    try:
        soup = soup[-1]
    except:
        pass
    soup = soup.find_all('a')
    soup = soup[-1].get('href')
    return soup


def parser_website(link):
    links = []
    html = f.get_html(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    soup = soup.find_all('a', class_='zag21')
    for sou in soup:
        links.append(host + sou.get('href'))
    return links


def get_orenburg():
    links = []
    people = []
    log.debug(f'Parsing https://orenburg.arbitr.ru/')
    html = f.get_html('https://orenburg.arbitr.ru/about/ourJudges/aleksandrov')
    soup = BeautifulSoup(html.text, 'html.parser')
    soup = soup.find('div', class_='l-columns')
    soup = soup.find('div', class_='l-column l-column--left js-column')
    soup = soup.find('ul', class_='b-menu js-menu menu')
    soup = soup.find('div', class_='b-submenu js-submenu b-submenu--all')
    soup = soup.find('ul', class_='b-menu js-menu menu')
    soup = soup.find_all('li')
    for sou in soup:
        sou = sou.find('a', class_='item_link')
        if sou != None:
            links.append({"link":'https://orenburg.arbitr.ru' + sou.get('href'), "name": sou.get_text()})
    for link in links:
        people.append(parser_person(link, 'https://orenburg.arbitr.ru/'))
    return people

def parser():
    log.debug(f"The script {__name__} starts working")
    links = []
    people = []
    html = f.get_html(url)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        soup = soup.find_all(class_='menu2')
        for sou in soup:
            links.append(host+sou.get('href'))
        for link in links:
            website_links = parser_website(link)
            for website_link in website_links:
                direct_link = parser_direct_link(website_link)+'/'
                log.debug(f'Parsing {direct_link}')
                i = 0
                while i<3:
                    try:
                        people_links = parser_people_links(direct_link)
                        i=4
                    except:
                        if i == 2:
                            if direct_link.find('perm') != -1 :
                                pass
                            elif direct_link.find('orenburg') != -1:
                                pass
                            else:
                                return [{'code': 1, 'script': os.path.basename(__file__)}]

                        people_links = None
                        i+=1
                        log.warning(f'Duplicate or non-templated html at -> {direct_link}')
                if people_links != None:
                    for person_link in people_links:
                        if person_link != None:
                            person = parser_person(person_link, direct_link)
                            if person != 1:
                                people.append(person)
                            else:
                                return [{'code': 1, 'script': os.path.basename(__file__)}]
        log.debug('Parsing https://ipc.arbitr.ru/')
        people_links = parser_people_links('https://ipc.arbitr.ru/')
        for person_link in people_links:
            if person_link != None:
                person = parser_person(person_link, 'https://ipc.arbitr.ru/')
                if person != 1:
                    people.append(person)
        people.extend(get_orenburg())
        log.debug("The script stops working")
        return people
    else:
        return [{'code': 2, 'script': os.path.basename(__file__)}]

if __name__ == '__main__':
    print(parser())