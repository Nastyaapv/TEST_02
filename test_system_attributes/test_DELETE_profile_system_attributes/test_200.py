import allure

from conftest import *
from functions import gen_system_attributes, params_record_db_condition, parse_response_json, assert_status_code, \
    check_response_schema, count_record_db_condition
from json_schemas import schema_404_error


@allure.epic("Удаление системного атрибута")
@allure.description('Удаление системного атрибута')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test200:
    
    @allure.epic("Удаление системного атрибута")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52142")
    @pytest.mark.smoke
    def test_c52142_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52142")
        logging.info("Удаление системного атрибута. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 2
        
        # Вызов функции генерации системного атрибута
        system_attributes_json_names = gen_system_attributes(profile_api, i)[0]
        
        # Получаем параметр в БД условию
        system_attributes_id = params_record_db_condition(dbCursor, "id", "system_attribute",
                                                          f"json_name = '{system_attributes_json_names}'")
        
        params = {
            "id": system_attributes_id
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/system-attributes/delete",
                params = params)  # Записываем ответ метода в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        params = {
            "jsonName": f"{system_attributes_json_names}"
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
                                                         f"json_name = '{system_attributes_json_names}'")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД нет удаленной записи "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД одна или больше записей "
            logging.info(f"В БД удалилась запись.")
        logging.info(f"Тест завершен успешно.")
    
    ###############################################################################
    
    @allure.epic("Удаление системного атрибута")
    @allure.feature('Проверка кода 200')
    @allure.story('Использовать jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58264")
    def test_c58264_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58264")
        logging.info("Удаление системного атрибута. Использовать jsonName в качестве идентификатора")
        
        # Номер итерации для генерации данных
        i = 2
        
        # Вызов функции генерации системного атрибута
        system_attributes_json_names = gen_system_attributes(profile_api, i)[0]
        
        # Получаем параметр в БД условию
        params_record_db_condition(dbCursor, "id", "system_attribute",
                                   f"json_name = '{system_attributes_json_names}'")
        
        params = {
            "id": system_attributes_json_names,
            "useJsonNameAsId": True
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/system-attributes/delete",
                params = params)  # Записываем ответ метода в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        params = {
            "jsonName": f"{system_attributes_json_names}"
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
                                                         f"json_name = '{system_attributes_json_names}'")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД нет удаленной записи "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД одна или больше записей "
            logging.info(f"В БД удалилась запись.")
        logging.info(f"Тест завершен успешно.")
