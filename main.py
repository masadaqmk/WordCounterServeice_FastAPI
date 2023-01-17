from fastapi import FastAPI
from pydantic import BaseModel
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


app = FastAPI()


class Site(BaseModel):
    name: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_total_words_check_one(url):
    if not url:
        return {"message": "Please enter url"}
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://wordcounter.net/website-word-count")

        input_btn = driver.find_element(By.ID, "url")
        input_btn.send_keys(url)
        sub = driver.find_element(By.XPATH, "/html/body/div[6]/div/form/div/div[2]/input")
        sub.click()
        time.sleep(10)

        data = driver.find_element(By.ID, "word_count_block")
        if data:
            total_count = data.find_element(By.CLASS_NAME, "total-word-count").text
            total = [int(s) for s in total_count.split() if s.isdigit()]
            driver.close()
            return total[0]
        return 0
    except Exception as e:
        return 0


def get_total_words_check_two(url):
    if not url:
        return {"message": "Please enter url"}
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://www.searchbloom.com/tools/bulk-web-page-word-count-checker/")

        time.sleep(1)
        input_btn = driver.find_element(By.NAME, "urls")
        input_btn.send_keys(url)
        sub = driver.find_element(By.CLASS_NAME, "tool--btn-default")
        sub.submit()
        time.sleep(4)
        data = driver.find_element(By.CLASS_NAME, "data_url")
        table_data = data.find_elements(By.TAG_NAME, 'tr')
        _, m = table_data
        table_value = str(m.text)
        table_values = table_value.split()
        word_count_total = table_values[2]
        return word_count_total
    except Exception as e:
        return 0


@app.get("/site")
def say_hello(site: Site):
    url = site.name
    check_1 = get_total_words_check_one(url)
    if check_1 == 0:
        check_1 = get_total_words_check_two(url)

    return check_1

