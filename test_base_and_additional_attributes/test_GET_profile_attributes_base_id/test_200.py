import allure
import jmespath
from functions import check_response_schema, gen_test_base_attribute_id, parse_response_json, assert_status_code, \
    reformatted_param, params_record_db_condition

from conftest import *
from json_schemas import GET_profile_attributes_base_id_200_main_schema


@allure.epic("Получение информации о базовом атрибуте")
@allure.description('Получение информации о базовом атрибуте')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test200:
    
    @allure.epic("Получение информации о базовом атрибуте")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55342")
    @pytest.mark.smoke
    def test_c55342_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55342")
        logging.info("Получение информации о базовом атрибуте. Прямой сценарий")
        
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_name_new
        
        # Генерим базовый атрибут
        profile_attributes_base_id = gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Параметры тела ответа
        params = {
            "useJsonNameAsId": False
        }
        
        response = profile_api.get(f"/profile/attributes/base/{profile_attributes_base_id}",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_id_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[
                    key], 'base_attribute', f"id = {profile_attributes_base_id}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получение информации о базовом атрибуте")
    @allure.feature('Проверка кода 200')
    @allure.story('Использовать jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55346")
    def test_c55346_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55346")
        logging.info("Получение информации о базовом атрибуте. Использовать jsonName в качестве идентификатора")
        
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_name_new
        
        # Генерим базовый атрибут
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Параметры тела ответа
        params = {
            "useJsonNameAsId": True
        }
        
        response = profile_api.get(f"/profile/attributes/base/{base_attribute_json_name_new[i]}",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_id_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[
                    key], 'base_attribute', f"json_name = '{base_attribute_json_name_new[i]}'")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        logging.info(f"Тест завершен успешно.")
