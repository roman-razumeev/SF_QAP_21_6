import sys
import pytest
import requests
from api import PetFriends
from settings import BASE_URL
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password
import os
from tests.conftest_probe import minversion
from tests.conftest import add_headers_tofile

pf = PetFriends()

@add_headers_tofile  # применяем наш декоратор!
def test_get_api_key():
    """ Проверяем что запрос api ключа возвращает статус 200 и в ответе содержится слово key"""

    # Сохраняем полученный ответ с кодом статуса в status, а текст ответа в result:
    status, result = add_headers_tofile(valid_email, valid_password)

    # Сверяем полученные данные с нашими ожиданиями:
    assert status == 200
    assert 'key' in result

class TestClassPetFriends:
    """Class has scenery:
     - get list of pets
     - add pet (info + photo)
     - change pet info
     - delete pet"""

    @pytest.mark.skip (reason="Список всех 'не моих' питомцев слишком велик, пропускаем тест")
    def test_getAllPets(self, get_key, filter = ''):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
                        Для этого сначала получаем api ключ и сохраняем в переменную auth_key.
                        Далее используя этого ключ запрашиваем список всех питомцев и проверяем
                        что список не пустой. Доступное значение параметра filter - 'my_pets'
                        либо '' """

        status, result = pf.get_list_of_pets(get_key, filter)

        assert status == 200, 'Запрос выполнен неуспешно'

        assert len(result['pets']) > 0, 'Количество питомцев ' \
                                        'не соответствует ожиданиям'
        # assert content.get('Content-Type') == 'application/json'


    def test_getMyPets(self, get_key):

        filter = 'my_pets'
        status, result = pf.get_list_of_pets(get_key, filter)
        assert status == 200, 'Запрос выполнен неуспешно'
        assert len(result['pets']) > 0, 'Количество питомцев ' \
                                        'не соответствует ожиданиям'

    @pytest.mark.api
    @pytest.mark.event
    def test_add_new_pet_with_valid_data(self, get_key,
                                         name = 'Sharik',
                                         animal_type = 'dvorterier',
                                         age = '4',
                                         pet_photo = 'images/dog01.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""


        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join (os.path.dirname (__file__), pet_photo)
        # Добавляем питомца
        status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200, "Request hasn't executed successfully"
        assert result['name'] == name


    def test_successful_update_self_pet_info(self, get_key,
                                             name='Barboskin',
                                             animal_type='dog',
                                             age=5):
        """Checking possibility of pets update"""

        # Получаем ключ auth_key и список своих питомцев
        _, my_pets = pf.get_list_of_pets (get_key, "my_pets")

        # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
        if len (my_pets['pets']) > 0:
            status, result = pf.update_pet_info (get_key,
                                                 my_pets['pets'][0]['id'],
                                                 name, animal_type, age)
            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['name'] == name
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом
            # об отсутствии своих питомцев
            raise Exception ("There is no my pets")


    def test_successful_delete_self_pet(self, get_key):
        """Check possibility of pets deletion"""

        # Запрашиваем список своих питомцев
        filter = 'my_pets'
        status, my_pets = pf.get_list_of_pets(get_key, filter)

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(get_key, "Суперкот", "кот", "3", "images/cat1.jpg")
            _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(get_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()



class TestClassNewPetSimple:

    pet_id = None

    def test_add_new_pet_simple_valid_data(self, get_key,
                                           name='Барсик',
                                           animal_type='дворокот',
                                           age='6'):
        """Проверяем, что можно добавить питомца без фото с корректными данными"""

        # Добавляем питомца
        status, result = pf.add_new_pet_simple (get_key, name,
                                                animal_type, age)
        global pet_id
        pet_id = result['id']
        # print (f'\n!!! pet_id = {pet_id}')

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['pet_photo'] is ''


    def test_add_pet_photo_valid_data(self,
                                      get_key,
                                      pet_photo='images/cat1.jpg'):
        """Проверяем возможность добавления/замены фото
        существующему питомцу"""


        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        pet_photo = os.path.join(os.path.dirname (__file__), pet_photo)

        # Если список пустой, то пробуем вначале добавляем нового питомца
        # и получаем список заново
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple (get_key, "Барсик", "жук", "4")
            _, my_pets = pf.get_list_of_pets (get_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на
        # добавление фотографии
        status, result = pf.add_pet_photo (get_key,
                                           my_pets['pets'][0]['id'],
                                           pet_photo)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert 'pet_photo' in result

    def test_getMyPets(self, get_key):

        filter = 'my_pets'
        status, result = pf.get_list_of_pets(get_key, filter)
        # print(f'\nPets list: {result}')
        # print(f'{result.values()}')
        assert status == 200, 'Запрос выполнен неуспешно'
        assert len(result['pets']) > 0, 'Количество питомцев ' \
                                        'не соответствует ожиданиям'


    def test_successful_delete_self_pet(self, get_key):
        """Check possibility of pets deletion"""
        global pet_id

        if pet_id:
            _, result = pf.delete_pet(get_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        status, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев
        # нет id удалённого питомца
        assert status == 200
        assert self.pet_id not in my_pets.values()

#################################################
#  Ещё 10 вариантов тестов в одном классе
#################################################

# Test_1
class TestFullClassPetsFriends:

    def test_add_new_pet_nophoto_valid_data(self,
                                             get_key,
                                             name='Барсик',
                                             animal_type='дворокот',
                                             age='6'):
        """Проверяем что можно добавить питомца без фото с
        корректными данными"""

        # Добавляем питомца
        status, result = pf.add_new_pet_simple(get_key,
                                               name,
                                               animal_type,
                                               age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['pet_photo'] is ''

    # Test_2
    def test_add_pet_photo_valid_data(self,
                                      get_key,
                                      pet_photo='images/cat1.jpg'):
        """Проверяем возможность добавления/замены фото
        существующему питомцу"""

        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        pet_photo = os.path.join(os.path.dirname (__file__), pet_photo)

        # Если список пустой, то пробуем вначале добавляем нового питомца
        # и получаем список заново
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple (get_key, "Барсик", "жук", "4")
            _, my_pets = pf.get_list_of_pets (get_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на
        # добавление фотографии
        status, result = pf.add_pet_photo (get_key,
                                           my_pets['pets'][0]['id'],
                                           pet_photo)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert 'pet_photo' in result

    # Test_3
    def test_add_new_pet_simple_invalid_age(self,
                                            get_key,
                                            name='JPMorgan',
                                            animal_type='cat',
                                            age='#@%$'):
        """Проверяем что можно добавить питомца без фото с
        некорректными данными - символы вместо чисел возраста"""

    #     Добавляем питомца
        status, result = pf.add_new_pet_simple(get_key,
                                               name,
                                               animal_type,
                                               age)
        assert status == 200

    # Test_4
    def test_add_new_pet_invalid_symbols(self,
                                         get_key,
                                         name='ASD#^',
                                         animal_type='$%DDdd',
                                         age='5',
                                         pet_photo='images/dog01.jpg'):
        """Проверяем что можно ли добавить питомца со спецсимволами в имени и типе"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Добавляем питомца
        status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type

    # Test_5
    def test_add_pet_with_empty_value_in_variable_name(self,
                                                       get_key,
                                                       name='',
                                                       animal_type='cat',
                                                       age='2',
                                                       pet_photo='images/cat1.jpg'):
        """Проверка возможность добавления питомца с пустым значением
        в переменной name"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == ''

    # Test_6
    def test_get_api_key_for_invalid_username(self,
                                              email=invalid_email,
                                              password=valid_password):
        """ Проверяем что запрос api ключа с несуществующим именем пользователя
         возвращает статус 403 и в результате содержится строка
         'This user wasn&#x27;t found in database'"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'This user wasn&#x27;t found in database' in result

    # Test_7
    def test_get_api_key_for_invalid_password(self,
                                              email=valid_email,
                                              password=invalid_password):
        """ Проверяем что запрос api ключа с неправильным паролем возвращает статус 403
        и в результате содержится строка 'This user wasn&#x27;t found in database'"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'This user wasn&#x27;t found in database' in result

    # Test_8
    @pytest.mark.skip(reason="Пропускаем для тестирования параметра 'skip' ")
    def test_get_all_pets_with_invalid_key(self,
                                           filter=''):
        """Проверяем, что запрос всех питомцев с неверным api ключом возвращает код 403"""
        # Задаем неверный ключ api и сохраняем в переменную auth_key
        auth_key = {'key': '123'}
        # Запрашиваем список питомцев
        status, result = pf.get_list_of_pets(auth_key, filter)
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 403

    # Test_9
    @pytest.mark.xfail(reason="В базе данных пока не применим filter='qwerty'")
    def test_get_all_pets_with_incorrect_filter(self,
                                                filter='qwerty'):
        """ Проверяем что запрос питомцев c некорректным значением поля filter возвращает ошибку.
        Доступное значение параметра filter - 'my_pets' либо '' """

        # Получаем ключ auth_key и запрашиваем список питомцев с неправильным фильтром
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.get_list_of_pets(auth_key, filter)

        assert status == 500
        assert 'Filter value is incorrect' in result


    # Test_10
    def test_get_my_pets_with_valid_key(self,
                                        filter='my_pets'):
        """ Проверяем что запрос своих питомцев возвращает не пустой список.
        Доступное значение параметра filter - 'my_pets' либо '' """

        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, filter)

        # Проверяем - если список своих питомцев пуст, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(auth_key, 'Барсик', 'Кот', '6')
            _, my_pets = pf.get_list_of_pets(auth_key, filter)

        assert _ == 200
        assert len(my_pets['pets']) > 0

    # Test 11 - delete all
    def test_delete_all(self, get_key, filter = 'my_pets'):
        """Check possibility of all pets deletion"""

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(get_key, filter)
        # Если список питомцев не ноль, то запуск цикла удаления
        if len (my_pets['pets']) > 0:
            for pet in range(len (my_pets['pets'])-1):
                pf.delete_pet (get_key, my_pets['pets'][pet]['id'])
        else:
            print (f'List of my_pets is empty!!')

        # Ещё раз запрашиваем список своих питомцев
        status, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Проверяем что статус ответа равен 200
        assert status == 200
        assert len (my_pets['pets']) == 1

