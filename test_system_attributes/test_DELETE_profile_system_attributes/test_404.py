import allure

from conftest import *
from functions import count_record_db_condition, check_response_schema, assert_status_code, parse_response_json
from json_schemas import schema_404_error


@allure.epic("Удаление системного атрибута")
@allure.description('Удаление системного атрибута')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test404:
    
    @allure.epic("Удаление системного атрибута")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52143")
    def test_c52143_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52143")
        logging.info("Удаление системного атрибута. Несуществующий id")
        
        params = {
            "id": system_attributes_id_int_wrong
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/system-attributes/delete",
                params = params)  # Записываем ответ метода в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        params = {
            "id": f"{system_attributes_id_int_wrong}"
        }
        response = profile_api.get("/profile/system-attributes/get",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'system_attribute',
                                                         f"id = '{system_attributes_id_int_wrong}'")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД нет записи "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД одна или больше записей "
            logging.info(f"В БД нет записей.")
        logging.info(f"Тест завершен успешно.")
    
    ###############################################################################
    
    @allure.epic("Удаление системного атрибута")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58265")
    def test_c58265_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58265")
        logging.info("Удаление системного атрибута. Несуществующий jsonName в качестве идентификатора")
        
        params = {
            "id": system_attributes_jsonNames_wrong,
            "useJsonNameAsId": True
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/system-attributes/delete",
                params = params)  # Записываем ответ метода в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        params = {
            "jsonName": f"{system_attributes_jsonNames_wrong}"
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
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'system_attribute',
                                                         f"json_name = '{system_attributes_jsonNames_wrong}'")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД нет записи "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД одна или больше записей "
            logging.info(f"В БД нет записи.")
        logging.info(f"Тест завершен успешно.")
