#import urllib2
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")

def getStockData(symbols):
    stockData = {}
    for sym in symbols:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        url = "https://www.stockconsultant.com/consultnow/basicplus.cgi?symbol=" + sym
        supports = []
        resistances = []

        try:
            driver.get(url)
        except Exception:
            print("Error: cannot pull webpage of " + sym)
            continue

        for x in range(8, 17):
            try:
                ele_string = "/html/body/div[@class='containerborder']/div[20]/div["+str(x)+"]"
                ele = driver.find_element_by_xpath(ele_string)
                text = ele.text
            except Exception:
                print("Error on "+str(x))
                continue
                
            if len(text) > 0 and text[0] == '-':
                supports.append(text)
            elif len(text) > 0 and text[0] == '+':
                resistances.append(text)

        driver.close()
        driver.quit()

        supnums = []
        resnums = []

        for sup in supports:
            supnums.append(sup.split()[2])
        for res in resistances:
            resnums.append(res.split()[2])

        supstrength = []
        resstrength = []

        for sup in supports:
            supstrength.append(sup.split()[-1])
        for res in resistances:
            resstrength.append(res.split()[-1])

        sups = []
        ress = []
        for sup in supports:
            sups.append((sup.split()[2], sup.split()[-1]))
        for res in resistances:
            ress.append((res.split()[2], res.split()[-1]))
        
        stockData[sym] = {"Supports" : sups, "Resistances" : ress}

    return stockData

"""
test_page = 'https://www.stockconsultant.com/consultnow/basicplus.cgi?symbol=AMD'
html_page = urllib2.urlopen(test_page)
beaut_soup = BeautifulSoup(html_page, 'html.parser')
"""