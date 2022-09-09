from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверка, что запрос auth_key имеет статус 200 и содержит ключ 'key' в ответе"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_valid_auth_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список. Сначала получаем auth_key,
    затем проверяем, что статус код запроса 200 и полученный список не пустой.
    Параметр filter='' , если необходим список всех животных на сайте, 'my_pets',
    если только животных конкретного авторизованного юзера"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_valid_auth_key(name='Tar-Tar', animal_type='cat', age='10', pet_photo='../images/grumpy1.jpg'):
    """Проверяем, что можно добавить животное с корректными данными. Сначала получаем auth_key, затем создаем животное
    и проверяем статус-код, а также соответствие заданного имени в ответе сервера"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_update_info_of_valid_users_pet_wtih_valid_id(filter='my_pets'):
    """Проверяем возможность обновления информации о питомце, а также список питомцев с фильтром 'my_pet' на отсутствие
    питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter)
    if len(result['pets']) > 0:
        pet_id = result['pets'][0]['id']
        name, animal_type, age = result['pets'][0]['name'] + '1', result['pets'][0]['animal_type'] + '1', \
                                 result['pets'][0]['age'] + '1'
        status, my_pet = pf.update_info_about_pet(auth_key, pet_id, name, animal_type, age)

        assert status == 200
        assert my_pet['name'] == name
    else:
        raise Exception('There is no my pets')


def test_add_pet_simple_with_valid_auth_key(name='Tar-Tar', animal_type='cat', age='10'):
    """Проверяем, что можно добавить животное с корректными данными. Сначала получаем auth_key, затем создаем животное
    и проверяем статус-код, а также соответствие заданного имени в ответе сервера"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_valid_users_pet_wtih_valid_id(pet_photo='../images/grumpy2.jpg'):
    """Проверяем список my_pets на пустоту (вызываем исключение, если пустой), если питомец есть - добавляем фото,
    а также проверяем имя питомца до и после обновления"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')

    if len(result['pets']) > 0:
        pet_id = result['pets'][0]['id']

        status, my_pet = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pets'][0]['name'] == my_pet['name']
    else:
        raise Exception('There is no my pets')


def test_delete_pet_of_valid_user_with_valid_auth_key(filter='my_pets'):
    """Получаем список животных с фильтром my_pets, затем создаем новое животное с заданными параметрами
    если список пустой, иначе удаляем первое животное из списка. Проверяем статус-код запроса, а также наличие
    удаленного id у животного в повторно полученном списке"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter)
    if len(result['pets']) == 0:
        pf.add_new_pet(auth_key, name='Tar-Tar', animal_type='cat', age='10', pet_photo='../images/grumpy2.jpg')
        _, result = pf.get_list_of_pets(auth_key, filter)
    pet_id = result['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, filter)

    try:
        search_delete_pet_id = pet_id not in my_pets['pets'][0].values()
    except IndexError:
        search_delete_pet_id = True

    assert status == 200
    assert search_delete_pet_id


def test_get_api_key_for_invalid_user(email='test@mail.ru', password='test_password'):
    """Проверка, что при использовании невалидных данных статус-код 403, а также ответ не содержит ключ 'key'
    в ответе"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_valid_user_with_invalid_password(email=valid_email, password='test_password'):
    """Проверка, что при использовании валидной почты и невалидного пароля статус-код 403, а также ответ не содержит
    ключ 'key' в ответе"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_invalid_user_with_valid_password(email='test_email', password=valid_password):
    """Проверка, что при использовании валидной почты и невалидного пароля статус-код 403, а также ответ не содержит
    ключ 'key' в ответе"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_list_of_pets_invalid_auth_key(auth_key={'key': 'test_key'}, filter=''):
    """Проверяем, что запрос всех питомцев с использованием невалидного auth_key дает ошибку 403, а слово 'Forbidden'
    находится в ответе сервера."""

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'Forbidden' in result


def test_get_list_of_my_pets_invalid_auth_key(auth_key={'key': 'test_key'}, filter='my_pets'):
    """Проверяем, что запрос с фильтром 'my_pets' питомцев с использованием невалидного auth_key дает ошибку 403,
    а слово 'Forbidden' находится в ответе сервера."""

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'Forbidden' in result


def test_get_list_of_pets_valid_auth_key_invalid_filter(filter='test'):
    """Проверяем, что запрос с некорректным фильтром 'test' с использованием валидного auth_key дает ошибку 500,
    а слово 'Internal Server Error' присутствует в ответе сервера."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500
    assert 'Internal Server Error' in result


def test_add_new_pet_invalid_auth_key(auth_key={'key': 'test_key'}, name='Tar-Tar', animal_type='cat', age='10',
                                      pet_photo='../images/grumpy1.jpg'):
    """Проверяем, что нельзя добавить животное с корректными данными, но с невалидным auth_key. Создаем животное
    и проверяем статус-код, а также наличие 'Forbidden' и в ответе сервера"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert 'Forbidden' in result


# Критический баг! Есть возможность обновлять информацию о чужих питомцах!
def test_update_info_of_valid_users_pet_with_valid_id(filter=''):
    """Проверяем возможность обновления информации о чужом питомце, ожидаем, что статус-код будет 403, а текст ответа
    содержать 'Forbidden'"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter)

    pet_id = result['pets'][0]['id']
    name, animal_type, age = result['pets'][0]['name'] + '1', result['pets'][0]['animal_type'] + '1', \
                             result['pets'][0]['age'] + '1'
    status, result = pf.update_info_about_pet(auth_key, pet_id, name, animal_type, age)

    assert status == 403
    assert 'Forbidden' in result


# Критический баг! Есть возможность удалять чужих питомцев!
def test_delete_anothers_pet_with_valid_auth_key(filter=''):
    """Проверяем возможность удаления чужого питомца, ожидаем, что статус-код будет 403, а текст ответа
    содержать 'Forbidden'"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter)

    pet_id = result['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, filter)

    if len(my_pets['pets']) > 0:
        search_delete_pet_id = pet_id not in my_pets['pets'][0].values()
    else:
        search_delete_pet_id = True

    assert status == 403
    assert not search_delete_pet_id


def test_add_photo_anothers_pet_with_valid_auth_key(pet_photo='../images/grumpy2.jpg'):
    """Проверяем возможность обновления фото чужого питомца с использованием валидного auth_key, ожидаем ошибку 500"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter='')

    pet_id = result['pets'][-1]['id']
    status, my_pet = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 500
