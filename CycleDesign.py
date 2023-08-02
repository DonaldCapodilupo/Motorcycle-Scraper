class CycleDesignCrawler:
    def __init__(self):
        pass


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup

links_To_Scrape = {'Craigslist':
                       [
                           "https://boston.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
                           "https://worcester.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
                           "https://westernmass.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
                           "https://capecod.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50",
                           'https://southcoast.craigslist.org/search/mca?purveyor-input=all&condition=20&condition=30&condition=40&condition=50'
                           ],
                   'Cycle Design': ["https://www.cycledesignonline.com/default.asp?page=xPreOwnedInventory"],
                   'Central Mass Powersport': ["https://www.newenglandpowersports.com/preowned"]
                   }

# Code to make selenium headless.
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

page = driver.get("https://www.cycledesignonline.com/default.asp?page=xPreOwnedInventory")

html = driver.page_source

print(html)

soup = BeautifulSoup(html, "html.parser")

#print(soup)

print()

print(soup.find_all('href'))

#for elements in driver.find_elements_by_tag_name('a'):
#    print(elements)
#    href = elements.get_attribute('href')
#    print(href)
#    if href is not None and "www." in href:
#        print("Proper elements found - scraping: " + " - New England PowerSports")

