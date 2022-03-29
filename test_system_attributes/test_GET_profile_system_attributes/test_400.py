import allure

from conftest import *
from functions import assert_status_code, count_record_db, parse_response_json, check_response_schema
from json_schemas import schema_400_error


@allure.epic("Получение системного атрибута по его json name")
@allure.description('Получение системного атрибута по его json name')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test400:
    
    @allure.epic("Получение системного атрибута по его json name")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указывать jsonName')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/56509")
    def test_c56509_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/56509")
        logging.info("Получение системного атрибута по его json name. Не указывать jsonName")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'system_attribute')
        
        response = profile_api.get("/profile/system-attributes")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_after = count_record_db(dbCursor, 'system_attribute')
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД кол-во записей не изменилось"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"В БД одна или больше записей "
            logging.info(f"В БД кол-во записей не изменилось")
        
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    @allure.epic("Получение системного атрибута по его json name")
    @allure.feature('Проверка кода 400')
    @allure.story('Пустой jsonName')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/56511")
    def test_c56511_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/56511")
        logging.info("Получение системного атрибута по его json name. Пустой jsonName")
        
        params = {
            "jsonName": f""
        }
        
        response = profile_api.get("/profile/system-attributes",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_400_error)  # Проверка JSON-схемы ответа
        
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
