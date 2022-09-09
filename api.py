from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import json


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str):
        """Получение auth_key, метод посылает GET API запрос и возвращает результат
        в виде кортежа статуса запроса и словаря с auth_key"""
        headers = {'email': email, 'password': password}
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str):
        """GET метод получает список всех питомцев с главной страницы. Чтобы получить список ваших
        питомцев, необходимо прописать filter=my_pets """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str):
        """POST Метод создает нового питомца с заданными данными: имя, тип животного, возраст,
        фотография питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str):
        """POST Метод создает нового питомца с заданными данными: имя, тип животного, возраст"""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name,
                'animal_type': animal_type,
                'age': age}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str):
        """Delete метод, который удаляет питомца из списка my_pets по pets_id. Возвращает
        статус код запроса и пустую строку (хотя должен сообщение об успешном удалении...)"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_info_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str):
        """PUT метод, отправляет запрос на сервер с новыми данными по питомцу (только имя, тип и возраст)
        и возвращает статус-код и result с обновленными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {'name': name,
                'animal_type': animal_type,
                'age': age}
        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str):
        """POST Метод добавляет фотографию питомца (если у питомца уже было фото - обновляет) и возвращает статус-код
        запроса и result с обновленными данными питомца"""

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
