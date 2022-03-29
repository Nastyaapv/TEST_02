import allure
from conftest import *
from functions import parse_response_json, assert_status_code, check_response_schema, count_record_db_condition
from json_schemas import schema_404_error


@allure.epic("Получение информации о дополнительном атрибуте")
@allure.description('Получение информации о дополнительном атрибуте')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test404:
    
    @allure.epic("Получение информации о дополнительном атрибуте")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52182")
    # https://git.dev-mcx.ru/zenit/profile-service/-/issues/41 - ИСПРАВИЛИ
    def test_c52182_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52182")
        logging.info("Получение информации о дополнительном атрибуте. Несуществующий id")
        
        # Указываем данные запроса
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_wrong}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что данных нет в БД"):
            # Получаем количество записей в БД по условию
            db_count = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"id = {additional_attribute_id_wrong}")
            
            assert db_count == 0, f"Количество записей в БД - {db_count}.\n" \
                                  f"Ожидаемое количество записей в БД - 0.\n"
        
        logging.info(f"Данных нет в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ###############################################################################################
    
    @allure.epic("Получение информации о дополнительном атрибуте")
    @allure.feature('Проверка кода 404')
    @allure.story('Некорректный jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55312")
    def test_c55312_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55312")
        logging.info("Получение информации о дополнительном атрибуте. Некорректный jsonName в качестве идентификатора")
        
        params = {
            "useJsonNameAsId": True
        }
        # Указываем данные запроса
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_json_name_wrong_str}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что данных нет в БД"):
            # Получаем количество записей в БД по условию
            db_count = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"json_name = '{additional_attribute_json_name_wrong_str}'")
            
            assert db_count == 0, f"Количество записей в БД - {db_count}.\n" \
                                  f"Ожидаемое количество записей в БД - 0.\n"
        
        logging.info(f"Данных нет в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ###############################################################################################
    
    @allure.epic("Получение информации о дополнительном атрибуте")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55310")
    def test_c55310_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55310")
        logging.info(
                "Получение информации о дополнительном атрибуте. Несуществующий jsonName в качестве идентификатора")
        
        params = {
            "useJsonNameAsId": True
        }
        # Указываем данные запроса
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_wrong_str}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что данных нет в БД"):
            # Получаем количество записей в БД по условию
            db_count = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"json_name = '{additional_attribute_id_wrong_str}'")
            
            assert db_count == 0, f"Количество записей в БД - {db_count}.\n" \
                                  f"Ожидаемое количество записей в БД - 0.\n"
        
        logging.info(f"Данных нет в БД.")
        logging.info(f"Тест завершен успешно.")
