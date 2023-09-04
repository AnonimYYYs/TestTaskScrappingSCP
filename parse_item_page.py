
"""
# Задайте URL сайта
url = 'https://www.ralphlauren.nl/en/men/clothing/hoodies-sweatshirts/10204?webcat=men%7Cclothing%7Cmen-clothing-hoodies-sweatshirts'
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# Указываем путь к расширению CRX
extension_path = "C:\\Users\\Nikita\\Downloads\\hipncndjamdcmphkgngojegjblibadbe.crx"

options = webdriver.EdgeOptions()

# Добавляем расширение в опции
options.add_extension(extension_path)
driver = webdriver.Edge(options=options)
driver.maximize_window()
# ----------------------------------------------


def get_both_images(url):
    driver.get(url)
    time.sleep(5)
    to_res = []
    slide_elements = driver.find_elements(By.XPATH,
                                          '//div[@class="swiper-slide " and (@data-slideindex="0" or @data-slideindex="1")]')

    for slide_element in slide_elements:
        zoom_container_element = slide_element.find_element(By.XPATH, './/div[@class="swiper-zoom-container  use-image-ratio"]')
        picture_element = zoom_container_element.find_element(By.XPATH, './/picture[@class="swiper-zoomable"]')
        img_element = picture_element.find_element(By.XPATH, './/img[@class="popup-img pdp-popup-img zoomable"]')
        img_src = img_element.get_attribute("data-img")
        to_res.append(img_src)

    return to_res


with open('main_parsed_updated.json', 'r') as file:
    data = json.load(file)  # Загружаем JSON данные из файла

counter = 0
toDo = True
for key, value in data.items():
    for url in value:
        if not value.get(url):
            pair = get_both_images(url)
            if not pair:
                toDo = False
                break
            counter += 1
            value[url] = pair
    if not toDo:
        break

with open('main_parsed_updated.json', 'w') as file:
    json.dump(data, file, indent=4)

print(counter)
driver.quit()
