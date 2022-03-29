import allure

from conftest import *
from functions import parse_response_json, assert_status_code, check_response_schema, count_record_db_condition
from json_schemas import schema_404_error


@allure.epic("Получение системного атрибута по его json name")
@allure.description('Получение системного атрибута по его json name')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test404:
    
    @allure.epic("Получение системного атрибута по его json name")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий jsonName')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/56508")
    def test_c56508_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/56508")
        logging.info("Получение системного атрибута по его json name. Несуществующий jsonName")
        
        params = {
            "jsonName": f"{additional_attribute_jsonNames_wrong}"
        }
        
        response = profile_api.get("/profile/system-attributes",
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
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'system_attribute',
                                                         f"json_name = '{additional_attribute_jsonNames_wrong}'")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД нет удаленной записи "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД одна или больше записей "
            logging.info(f"В БД удалилась запись.")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получение системного атрибута по его json name")
    @allure.feature('Проверка кода 404')
    @allure.story('Невалидный jsonName')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/56510")
    def test_c56510_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/56510")
        logging.info("Получение системного атрибута по его json name. Невалидный jsonName")
        
        params = {
            "jsonName": f"{invalid_symbol}"
        }
        
        response = profile_api.get("/profile/system-attributes",
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
        
        #  Не проверяем из-за ошибки psycopg2.errors.InvalidTextRepresentation: invalid input syntax for integer: "!@#$%^*()_:;?/>.<,"
        # # Получаем количество записей в БД по условию
        # # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        # count_record_db_cond = count_record_db_condition(dbCursor, 'system_attribute',
        #                                                  f"id = '{invalid_symbol}'")
        # # Проверяем наличие в БД по условию
        # with allure.step("Проверка того, что в БД нет записи "):  # Записываем шаг в отчет allure
        #     assert count_record_db_cond == 0, f"В БД одна или больше записей "
        #     logging.info(f"В БД нет записей.")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
