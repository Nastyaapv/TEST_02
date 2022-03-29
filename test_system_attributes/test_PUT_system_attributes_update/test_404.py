import allure

from conftest import *
from functions import *


@allure.epic("Изменение системного атрибута")
@allure.description("Изменение системного атрибута")
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test404:
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52113")
    def test_c52113_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52113")
        logging.info("Изменение системного атрибута. Несуществующий id")
        
        # Номер итерации для обновления данных
        j = 5
        
        body = {
            "required": system_attributes_required_new[j],
            "name": f"{system_attributes_name_new[j]}",
            "userType": system_attributes_userType_new[j],
            "metadata": system_attributes_metadata_new[j]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        params = {
            "id": f"{system_attributes_id_int_wrong}",
            "useJsonNameAsId": False
        }
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params, headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"id = {system_attributes_id_int_wrong}")
        
        with allure.step("Проверка того, что в БД нет записей"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД есть записи "
            logging.info(f"В БД нет записей.")
        
        # Todo можно добавить еще какую-то сверку с гетом например, не обязательно
        
        logging.info(f"Тест завершен успешно.")
    
    #####################################################################################################################################################
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58395")
    def test_c58395_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58395")
        logging.info("Изменение системного атрибута. Несуществующий jsonName в качестве идентификатора")
        
        # Номер итерации для обновления данных
        j = 2
        
        body = {
            "required": system_attributes_required_new[j],
            "name": f"{system_attributes_name_new[j]}",
            "userType": system_attributes_userType_new[j],
            "metadata": system_attributes_metadata_new[j]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        params = {
            "id": f"{system_attributes_jsonNames_wrong}",
            "useJsonNameAsId": True
        }
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params, headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"json_name = '{system_attributes_jsonNames_wrong}' and name = '{system_attributes_name_new[j]}'")
        
        with allure.step("Проверка того, что в БД нет записей"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД есть записи"
            logging.info(f"В БД нет записей.")
        
        params = {
            "jsonName": f"{system_attributes_jsonNames_wrong}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        logging.info(f"Тест завершен успешно.")
