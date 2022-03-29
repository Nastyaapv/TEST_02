import allure

from functions import check_response_schema, parse_response_json, assert_status_code, count_record_db_condition

from conftest import *
from json_schemas import schema_404_error


@allure.epic("Получение информации о базовом атрибуте")
@allure.description('Получение информации о базовом атрибуте')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test404:
    
    @allure.epic("Получение информации о базовом атрибуте")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55343")
    @pytest.mark.smoke
    def test_c55343_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55343")
        logging.info("Получение информации о базовом атрибуте. Несуществующий id")
        
        # Параметры тела ответа
        params = {
            "useJsonNameAsId": False
        }
        
        response = profile_api.get(f"/profile/attributes/base/{base_attribute_id_wrong}",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        # Получаем значение записи в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute', f"id = {base_attribute_id_wrong}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            assert count_record_db_cond == 0, f"Количество записей {count_record_db_cond}, должно быть: 0"
            logging.debug(f"В БД нет записей.")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получение информации о базовом атрибуте")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55347")
    def test_c55347_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55347")
        logging.info("Получение информации о базовом атрибуте. Несуществующий jsonName в качестве идентификатора")
        
        # Параметры тела ответа
        params = {
            "useJsonNameAsId": True
        }
        
        response = profile_api.get(f"/profile/attributes/base/{base_attribute_json_Name_wrong}",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        # Получаем значение записи в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"json_name = '{base_attribute_json_Name_wrong}'")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            assert count_record_db_cond == 0, f"Количество записей {count_record_db_cond}, должно быть: 0"
            logging.debug(f"В БД нет записей.")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получение информации о базовом атрибуте")
    @allure.feature('Проверка кода 404')
    @allure.story('Некорректный jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55348")
    def test_c55348_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55348")
        logging.info("Получение информации о базовом атрибуте. Некорректный jsonName в качестве идентификатора")
        
        # Параметры тела ответа
        params = {
            "useJsonNameAsId": True
        }
        
        response = profile_api.get(f"/profile/attributes/base/{invalid_symbol}",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        # Получаем значение записи в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"json_name = '{invalid_symbol}'")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            assert count_record_db_cond == 0, f"Количество записей {count_record_db_cond}, должно быть: 0"
            logging.debug(f"В БД нет записей.")
        logging.info(f"Тест завершен успешно.")
