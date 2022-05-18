import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element(by=By.ID, value='cookie')
timeout = time.time() + 5
five_min = time.time() + 60*5 # 5minutes

all_upgrade = driver.find_elements(by=By.CSS_SELECTOR, value='#store div')
all_upgrade_id = [upgrade.get_attribute('id')for upgrade in all_upgrade]
while True:
    cookie.click()
    if time.time() > timeout:
        all_upgrade_name_price = driver.find_elements_by_css_selector("#store b")
        upgrade_prices = []
        for upgrade_price in all_upgrade_name_price:
            element_text = upgrade_price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].replace(',',''))
                upgrade_prices.append(cost)

        cookie_upgrades = {}
        for _ in range(len(upgrade_prices)):
            cookie_upgrades[upgrade_prices[_]] = all_upgrade_id[_]

        money_element= driver.find_element(by=By.ID, value='money').text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        affordable_upgrades = {}
        for price, value in cookie_upgrades.items():
            if cookie_count > price:
                affordable_upgrades[price] = value
        max_buy = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[max_buy]
        driver.find_element(by=By.ID, value= to_purchase_id).click()
        timeout = time.time() + 5

        if time.time() > five_min:
            cookie_per_s = driver.find_element(by=By.ID, value="cps").text
            print(cookie_per_s)
            break





