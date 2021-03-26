from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from datetime import date


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


def get_Motorcycle_Information_Central_Mass_Powersport(url):
    page_Info = requests.get(url).text


    soup = BeautifulSoup(page_Info, 'html.parser')

    name = soup.find('div', class_='caption-container').text.strip()

    information_Table = soup.find_all('dl', 'dl-horizontal')
    right_Column = information_Table[1]
    left_column = information_Table[0]

    color = left_column.contents[23].text.strip()
    price = right_Column.contents[3].text.strip()
    mileage =  right_Column.contents[15].text.strip()

    information = [today, name,  price, "", color, mileage]
    return information


links_To_Scrape = ["https://www.newenglandpowersports.com/preowned","https://www.cycledesignonline.com/default.asp?page=xPreOwnedInventory"]
today = str(date.today())


if __name__ == '__main__':
    for website in links_To_Scrape:

        driver = webdriver.Chrome()
        driver.get(website)

        motorcycle_Links = []

        elems = driver.find_elements_by_tag_name('a')
        for link in elems:
            href = link.get_attribute('href')
            if href is not None:
                if href not in motorcycle_Links:
                    motorcycle_Links.append(href)

        for link in motorcycle_Links:
            if "https://www.cycledesignonline.com/" in link:
                try:
                    motorcycle_information = get_Motorcycle_Information_Cycle_Design(link)
                    with open('output.csv', 'a', newline='') as csv_File:
                        reader_obj = csv.writer(csv_File)
                        reader_obj.writerow(motorcycle_information)

                except (AttributeError, requests.exceptions.InvalidSchema) as error:
                    print("Link: " + link + " is not a link to a motorcycle.")
                    print(error)
                    pass

            elif "https://www.newenglandpowersports.com/" in link:
                if "pdf" in link:
                    continue
                try:
                    motorcycle_information = get_Motorcycle_Information_Central_Mass_Powersport(link)
                    with open('output.csv', 'a', newline='') as csv_File:
                        reader_obj = csv.writer(csv_File)
                        reader_obj.writerow(motorcycle_information)

                except (AttributeError, requests.exceptions.InvalidSchema) as error:
                    print("Link: " + link + " is not a link to a motorcycle.")
                    print(error)
                    pass

