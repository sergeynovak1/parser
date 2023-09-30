from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

url = 'https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod=581'


def get_html_with_selenium(url, javascript=False, time_sleep=None):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")

    s = Service(executable_path='./geckodriver')
    driver = webdriver.Firefox(service=s, options=options)

    if not javascript:
        options.add_argument("--disable-javascript")
    try:
        driver.get(url=url)
        if time_sleep:
            time.sleep(time_sleep)
        html_code = driver.page_source
    except Exception as _ex:
        html_code = ""
        print(_ex)
    finally:
        driver.close()
        driver.quit()
        return html_code


def get_avg_sum(url):
    content = get_html_with_selenium(url=url, time_sleep=5)

    soup = BeautifulSoup(content, 'html.parser')

    price_elements = [float(price_element.text) for price_element in soup.find_all('span', class_='price-amount')]

    avg = sum(price_elements) / len(price_elements)

    return round(avg, 2)


print(get_avg_sum(url=url))
