import allure
import jmespath

from conftest import *
from functions import parse_response_json, check_response_schema, gen_test_add_attribute_id, assert_status_code, \
    reformatted_param, params_record_db_condition
from json_schemas import GET_profile_attributes_additional_200_main_schema


@allure.epic("Получение информации о дополнительном атрибуте")
@allure.description('Получение информации о дополнительном атрибуте')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test200:
    
    @allure.epic("Получение информации о дополнительном атрибуте")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52181")
    @pytest.mark.smoke
    def test_c52181_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52181")
        logging.info("Получение информации о дополнительном атрибуте. Прямой сценарий")
        
        # Номер итерации для генерации данных additional_attribute_<param>_new
        i = 5
        
        # Вызов функции генерации дополнительного атрибута
        additional_attribute_id_new = gen_test_add_attribute_id(profile_api, dbCursor, i)[1]
        
        params = {
            "useJsonNameAsId": False
        }
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_new}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
        
        # with allure.step("Проверка что отобразились именно необходимые данные"):
        # 1. Проверяем сохранение данных в БД - dbCursor
        # 2. Для таблицы - FROM : "additional_attribute",
        # 3. По условию - WHERE : "name like '%{additional_attribute_name_new[j]}%' and json_name like '%{additional_attribute_jsonName_new[j]}%'
        # 4. Сверяем с - response_json
        # 5. Количество объектов (циклов повторений), для единичных объектов - 1
        # 6. Название словаря ключей json и БД
        # 7-<..>. Уровень вложенности словаря ключей json и БД
        # check_save_data_db(dbCursor, "additional_attribute",
        #                    f"id = {additional_attribute_id_new}",
        #                    response_json, param_ALL_additional_attribute)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for key in param_ALL_additional_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                json_value = reformatted_param(key, json_value)
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                      'additional_attribute',
                                                      f"id = {additional_attribute_id_new}")
                # Логирование, для отладки
                logging.debug(f"JSON-данные {json_value} - ключ {key}")
                logging.debug(f"БД-данные {db_query} - ключ БД {param_ALL_additional_attribute[key]}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получение информации о дополнительном атрибуте")
    @allure.feature('Проверка кода 200')
    @allure.story('Использовать jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55309")
    def test_c55309_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55309")
        logging.info("Получение информации о дополнительном атрибуте. Использовать jsonName в качестве идентификатора")
        
        # Номер итерации для генерации данных additional_attribute_<param>_new
        i = 5
        
        # Вызов функции генерации дополнительного атрибута
        additional_attribute_json_name = gen_test_add_attribute_id(profile_api, dbCursor, i)[0]
        
        params = {
            "useJsonNameAsId": True
        }
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_json_name}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for key in param_ALL_additional_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value)
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                      'additional_attribute',
                                                      f"json_name = '{additional_attribute_json_name}'")
                # Логирование, для отладки
                logging.debug(f"JSON-данные {json_value} - ключ {key}")
                logging.debug(f"БД-данные {db_query} - ключ БД {param_ALL_additional_attribute[key]}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
