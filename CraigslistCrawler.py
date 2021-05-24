from bs4 import BeautifulSoup
import requests
import csv
from datetime import date



def get_Motorcycle_Information_Craigslist(url):
    try:

        page_Info = requests.get(url).text

        soup = BeautifulSoup(page_Info, 'html.parser')
        try:
            title_Row = soup.find('span', class_='postingtitletext')
            motorcycle_name = title_Row.find('span',  id="titletextonly").text
            motorcycle_price = title_Row.find('span', class_="price").text

            information_Table = soup.find('div', class_='mapAndAttrs')
            bike_Information = information_Table.find_all('p', class_='attrgroup')

            #groups = bike_Information.find_next('p')



            for i in bike_Information:
                information_Dict = {
                    'condition': '',
                    'odometer': '',
                    'color': '',
                    'transmission': '',
                    'engine displacement': '',
                }
                for s in i.find_all():
                    if 'condition' in s.text:
                        information_Dict['condition'] = s.text[11:]

                    elif 'odometer: ' in s.text:
                        information_Dict['odometer'] = s.text[9:]
                    elif 'color: ' in s.text:
                        information_Dict['color'] = s.text[13:]
                    elif 'transmission: ' in s.text:
                        information_Dict['transmission'] = s.text[14:]
                    elif 'engine displacement: ' in s.text:
                        information_Dict['engine displacement'] = s.text[19:]

                if information_Dict['condition'] != '':
                    with open('Big Balls.csv', 'a', newline='') as csv_File:

                        #[today, name, price, stock_Number, color, mileage, transmission]
                        reader_obj = csv.writer(csv_File)
                        reader_obj.writerow([today, motorcycle_name, motorcycle_price, "", information_Dict['color'], information_Dict['odometer'],
                                             information_Dict['transmission'], information_Dict['engine displacement'],information_Dict['condition']])
        except (AttributeError, TypeError):
            pass
    except requests.exceptions.MissingSchema:
        pass










links_To_Scrape = {'Craigslist':
                       ["https://boston.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
                        "https://worcester.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
                        "https://westernmass.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
                        "https://capecod.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
                        'https://southcoast.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50'
                        ],
                   'Cycle Design':[],
                   'Central Mass Powersport':[]
}
today = str(date.today())



def craigslistCrawler():
    for website in links_To_Scrape['Craigslist']:

        reqs = requests.get(website)

        soup = BeautifulSoup(reqs.text, 'html.parser')

        href_tags = soup.find_all(href=True)

        hrefs = [tag.get('href') for tag in href_tags]

        hrefs_No_Duplicates = []

        for link in hrefs:
            if link not in hrefs_No_Duplicates:
                hrefs_No_Duplicates.append(link)




        for link in hrefs_No_Duplicates:
            try:
                get_Motorcycle_Information_Craigslist(link)
                print("Scraped: " + link)
            except UnicodeEncodeError:
                if link.title == 'next page':
                    links_To_Scrape['Craigslist'].append(link)
                pass





        #print(website)
        #driver = webdriver.Chrome()
        #driver.get(website)
        #motorcycle_Links = []
        #elems = driver.find_elements_by_tag_name('a')
        #for link in elems:
        #    if link.get_attribute('title')== "next page" and link.get_attribute('href') not in links_To_Scrape and link.get_attribute('href'):
        #            links_To_Scrape['Craigslist'].append(link.get_attribute('href'))
        #            break
        #    href = link.get_attribute('href')
        #    if href is not None:
        #        if href not in motorcycle_Links:
        #            motorcycle_Links.append(href)
        #for link in motorcycle_Links:
        #    try:
        #        get_Motorcycle_Information_Craigslist(link)
        #    except UnicodeEncodeError:
        #        if link.title == 'next page':
        #            links_To_Scrape['Craigslist'].append(link)
        #        pass
        #driver.close()



craigslistCrawler()