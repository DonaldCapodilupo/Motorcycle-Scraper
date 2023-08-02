import requests
import csv
from selenium import webdriver
from datetime import date
import os
from bs4 import BeautifulSoup

output_file = "Motorcycle Data.csv"

links_To_Scrape = {'Craigslist':
    [
        "https://boston.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
        "https://worcester.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
        "https://westernmass.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
        "https://capecod.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
        'https://southcoast.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50'
    ],
    'Cycle Design': [
        "https://www.cycledesignonline.com/default.asp?page=xPreOwnedInventory"
    ],
    'Central Mass Powersport':
        [
            "https://www.newenglandpowersports.com/preowned"
        ]
}
today = str(date.today())


def setupFiles():
    print(os.listdir())

    if "Historical Data" not in os.listdir():
        os.mkdir("Historical Data")


def write_Motorcycle_Information_To_CSV(motorcycle_information):
    with open(output_file, 'a', newline='') as csv_File:
        reader_obj = csv.writer(csv_File)
        reader_obj.writerow(motorcycle_information)


def get_Motorcycle_Information_Cycle_Design(url):
    page_Info = requests.get(url).text

    soup = BeautifulSoup(page_Info, 'html.parser')

    title_Section = soup.find('div', 'unitTitle')
    name = title_Section.find('h1').text

    price_Section = soup.find('div', 'unitPrice')
    price = price_Section.find('h2').text

    information_Table = soup.find('div', 'unitHighlights')
    more_Specific_Information_Table = information_Table.find('ul')

    proper_Row_Stock_Number = more_Specific_Information_Table.find('li', 'liUnit LiInvStockNumber')
    stock_Number = proper_Row_Stock_Number.find('span').text

    proper_Row_Color = more_Specific_Information_Table.find('li', 'liUnit LiInvColor')
    color = proper_Row_Color.find('span').text

    proper_Row_Mileage = more_Specific_Information_Table.find('li', 'liUnit LiInvMileage')
    mileage = proper_Row_Mileage.find('span').text

    proper_Row_Transmission = more_Specific_Information_Table.find('li', 'liUnit LiInvTransmission')
    transmission = proper_Row_Transmission.find('span').text

    information = [today, name, price, stock_Number, color, mileage, transmission]
    return information


def cycleDesignCrawler():
    from selenium.webdriver.chrome.options import Options
    for website in links_To_Scrape['Cycle Design']:
        # Code to make selenium headless.
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(website)

        for elements in driver.find_elements_by_tag_name('a'):
            href = elements.get_attribute('href')
            print(href)
            if href is not None and "www." in href:
                print("Proper elements found - scraping: " + website + " - New England PowerSports")
                try:
                    write_Motorcycle_Information_To_CSV(get_Motorcycle_Information_Cycle_Design(href))
                except AttributeError:
                    print('Just kidding - that one didn\'t work lol')


def get_Motorcycle_Information_Craigslist(url):
    try:

        page_Info = requests.get(url).text

        soup = BeautifulSoup(page_Info, 'html.parser')
        try:
            title_Row = soup.find('span', class_='postingtitletext')
            motorcycle_name = title_Row.find('span', id="titletextonly").text
            motorcycle_price = title_Row.find('span', class_="price").text

            information_Table = soup.find('div', class_='mapAndAttrs')
            bike_Information = information_Table.find_all('p', class_='attrgroup')

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
                    with open(output_file, 'a', newline='') as csv_File:
                        # [today, name, price, stock_Number, color, mileage, transmission]
                        reader_obj = csv.writer(csv_File)
                        reader_obj.writerow([today, motorcycle_name, motorcycle_price, "", information_Dict['color'],
                                             information_Dict['odometer'],
                                             information_Dict['transmission'], information_Dict['engine displacement'],
                                             information_Dict['condition']])
        except (AttributeError, TypeError):
            pass
    except requests.exceptions.MissingSchema:
        pass


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


def get_Motorcycle_Information_Central_Mass_Powersport(url):
    page_Info = requests.get(url).text

    soup = BeautifulSoup(page_Info, 'html.parser')

    try:
        name = soup.find('div', class_='caption-container').text.strip()
    except AttributeError:
        print("Attribute Error - Skipping")
        return []

    information_Table = soup.find_all('dl', 'dl-horizontal')
    right_Column = information_Table[1]
    left_column = information_Table[0]

    color = left_column.contents[23].text.strip()
    price = right_Column.contents[3].text.strip()
    mileage = right_Column.contents[15].text.strip()

    information = [today, name, price, "", color, mileage]
    return information


def scrape_New_England_PowerSports_Main_INV_Page(website, driver):
    a_Elements = driver.find_elements_by_tag_name('a')
    for elements in a_Elements:
        href = elements.get_attribute('href')
        if href is not None and "uDetail" in href:
            print("Proper elements found - scraping: " + website + " - New England PowerSports")
            motorcycle_information = get_Motorcycle_Information_Central_Mass_Powersport(href)
            write_Motorcycle_Information_To_CSV(motorcycle_information)


def newEnglandPowersportsCrawler():
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import StaleElementReferenceException

    for website in links_To_Scrape['Central Mass Powersport']:
        # Code to make selenium headless.
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(website)

        pages = int(
            driver.find_elements_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div/div[3]/span')[0].text[-1])

        next_Page_Button = driver.find_elements_by_xpath(
            '/html/body/div[2]/div/div[2]/div/div[1]/div/div[3]/span/span')[0]

        for page_num in range(pages):
            try:
                scrape_New_England_PowerSports_Main_INV_Page(website, driver)
                print('Moving on to page ' + str(page_num) + ". - New England PowerSport")
            except StaleElementReferenceException:
                print('StaleElementReferenceException, attempting to find a tags again.')
                scrape_New_England_PowerSports_Main_INV_Page(website, driver)
                print('Moving on to page ' + str(page_num) + ". - New England PowerSport")

            try:
                next_Page_Button.click()
            except StaleElementReferenceException:
                break


if __name__ == '__main__':
    setupFiles()

    #craigslistCrawler()
#
    #cycleDesignCrawler()
#
    newEnglandPowersportsCrawler()
