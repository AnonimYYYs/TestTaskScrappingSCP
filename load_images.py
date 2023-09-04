import os
import requests
import json

# Загрузить JSON-файл
with open("main_parsed_updated.json", "r") as json_file:
    data = json.load(json_file)

# Папка для сохранения изображений
image_folder = "images"

# Создать папки person и cloth, если их нет
for subfolder in ["person", "cloth"]:
    os.makedirs(os.path.join(image_folder, subfolder), exist_ok=True)

# Пройтись по ключам в JSON-файле
for key, value in data.items():
    # Создать папки для данного ключа внутри person и cloth
    person_folder = os.path.join(image_folder, "person", key)
    cloth_folder = os.path.join(image_folder, "cloth", key)
    os.makedirs(person_folder, exist_ok=True)
    os.makedirs(cloth_folder, exist_ok=True)

    ind = 0
    # Пройтись по вложенным ключам
    for inner_key, inner_value in value.items():
        ind += 1
        # Пройтись по ссылкам на изображения
        if inner_value:
            response = requests.get(inner_value[0])

            # Сохранить изображение, если запрос успешен
            if response.status_code == 200:
                image_extension = 'jpg'
                image_filename = f"{ind}.{image_extension}"
                image_path = os.path.join(person_folder, image_filename)
                # image_path = os.path.join(cloth_folder, image_filename)

                with open(image_path, "wb") as image_file:
                    image_file.write(response.content)

            response = requests.get(inner_value[1])

            # Сохранить изображение, если запрос успешен
            if response.status_code == 200:
                image_extension = 'jpg'
                image_filename = f"{ind}.{image_extension}"
                image_path = os.path.join(cloth_folder, image_filename)

                with open(image_path, "wb") as image_file:
                    image_file.write(response.content)