import sys
import csv
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox
from bs4 import BeautifulSoup
from dateutil import parser
from selenium import webdriver
from time import sleep

EBAY_URL = ''
CHROMEDRIVER_PATH = 'chromedriver'

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('eBay Scraper')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.keyword_label = QLabel('Enter Keyword:')
        self.keyword_input = QLineEdit()
        layout.addWidget(self.keyword_label)
        layout.addWidget(self.keyword_input)

        self.filter_label = QLabel('Select Filter:')
        self.filter_combo = QComboBox()
        self.filter_combo.addItem('All Listings')
        self.filter_combo.addItem('Best Offer')
        self.filter_combo.addItem('Auction')
        self.filter_combo.addItem('Buy It Now')
        layout.addWidget(self.filter_label)
        layout.addWidget(self.filter_combo)

        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search(self):
        keyword = self.keyword_input.text()
        filter_index = self.filter_combo.currentIndex()
        filters = {
            0: '',
            1: '&LH_BO=1',
            2: '&LH_Auction=1',
            3: '&LH_BIN=1'
        }.get(filter_index, '')

        try:
            scrape_ebay_data(keyword, filters)
        except Exception as e:
            self.log_error(str(e))

    def log_error(self, message):
        with open('error_log.txt', 'a') as f:
            f.write(message + '\n')

def init_driver():
    return webdriver.Chrome(CHROMEDRIVER_PATH)

def scrape_ebay_data(item, filters):
    driver = init_driver()
    url = construct_url(item, filters)

    global data_filters
    csv_file = open(f'{item}.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)

    page_num = 1
    while True:
        if 'Min_Price' in data_filters:
            min_price = '&_udlo={}'.format(data_filters['Min_Price'])
            max_price = '&_udlo={}'.format(data_filters['Max_Price'])
        
            if 'Format' in data_filters:
                format = data_filters['Format']
                url = f'{url}{format}{min_price}{max_price}&_ipg=200&_pgn={page_num}'
            else:
                url = f'{url}{min_price}{max_price}&_ipg=200&_pgn={page_num}'
        
        else:
            url = f'{url}&_ipg=200&_pgn={page_num}'

        driver.get(url)
        sleep(1.5)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        response = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(response,'html.parser')
        items = soup.find_all('li', class_='s-item')

        for item in items:
            try:
                title = item.find('h3', class_='s-item__title').text
            except Exception:
                continue

            try:
                item_type = item.find('span', class_='SECONDARY_INFO').text
            except Exception:
                item_type = 'None'

            try:
                price = item.find('span', class_='s-item__price').text
            except Exception:
                continue

            try:
                rs = item.find('span', class_='s-item__reviews-count').find('span').text
            except Exception:
                rs = 'None'

            sell_date = item.find('span', class_='POSITIVE').text.replace('Sold', '')
            t3 = parser.parse(str(sell_date))
            t4 = parser.parse(str(datetime.date.today()))
            c = t4 - t3
            days = round(c.total_seconds() / 86400)

            h = item.find('a')
            link = (h['href'], h.get_text(strip=True))
            link = list(link)[0]

            if 'Time' in data_filters:
                time = data_filters['Time']      
            else:
                time = 2     

            if days > time:
                csv_file.close()
                return menu()             
            
            writer.writerow(['Title', 'Type', 'Price', 'Reviews', 'Link'])
            writer.writerow([title, item_type, price, rs, link])

        page_num += 1

def construct_url(item, filters):
    url = EBAY_URL.format(item)
    url += filters
    return url

def settings():
    global data_filters

    choice = 0
    if choice == 1:
        min_price = int(input('Enter the Min Price (Ex: 20 [0 if None]): '))
        max_price = int(input('Enter the Max Price (Ex: 50 [0 if None]): '))
        data_filters['Min_Price'] = min_price
        data_filters['Max_Price'] = max_price
        return menu()
    
    elif choice == 2:
        time = int(input('Enter the Minimum Days (Ex: 2): '))
        data_filters['Time'] = time
        return menu()
    
    elif choice == 3:
        choice = 1  # Assume "All Listings" by default
        if choice == 1:
            return settings()
        elif choice == 2:
            data_filters['Format'] = '&LH_BO=1'
        elif choice == 3:
            data_filters['Format'] = '&LH_Auction=1'
        elif choice == 4:
            data_filters['Format'] = '&LH_BIN=1'
        else:
            return settings()
    
    elif choice == 4:
        return menu()

    else:
        return settings()
    
    return settings()

def menu():
    global data_filters

    keyword = ''
    filters = ''
    try:
        scrape_ebay_data(keyword, filters)
    except Exception as e:
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
