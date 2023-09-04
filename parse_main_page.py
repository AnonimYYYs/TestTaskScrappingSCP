import json
from bs4 import BeautifulSoup

# Открываем файл HTML в локальной директории
with open('main.html', 'r', encoding='utf-8') as file:
    content = file.read()

# Создаем объект BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Ищем все карточки объектов
cards = soup.find_all('div', class_='grid-tile js-category-grid-product ingridOneByOne')

# Создаем словарь для хранения данных
data_dict = {}

# Перебираем каждую карточку
for card in cards:
    # Ищем ссылку внутри тега <a class="thumb-link">
    thumb_link = card.find('a', class_='thumb-link')
    thumb_href = thumb_link['href']

    # Ищем текст внутри тега <a class="name-link"> и удаляем символы переноса строки
    name_link = card.find('a', class_='name-link')
    name_text = name_link.text.replace('\n', '')

    # Ищем список <ul class="swatch-list">
    swatch_list = card.find('ul', class_='swatch-list')

    # Если список существует, извлекаем ссылки
    if swatch_list:
        links = []
        swatch_items = swatch_list.find_all('a', attrs={"data-color": True})
        for item in swatch_items:
            color = item['data-color']
            links.append(f"{thumb_href}?color={color}")
    else:
        # Если списка нет, используем ссылку из thumb-link
        links = [thumb_href]

    # Добавляем ссылки в словарь, объединяя их, если ключ уже существует
    if name_text in data_dict:
        data_dict[name_text].extend(links)
    else:
        data_dict[name_text] = links

# Вывод словаря
print(data_dict)

# Сохраняем словарь в JSON-файл
with open('main_parsed.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


