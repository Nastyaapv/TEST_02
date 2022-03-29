import allure

from conftest import *
from functions import count_record_db, assert_status_code, parse_request_json, count_record_db_condition, \
    parse_response_json


@allure.epic("Добавление системного атрибута")
@allure.description('Добавление системного атрибута')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test400:
    
    @allure.epic("Добавление системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52106")
    @pytest.mark.smoke
    def test_c52106_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52106")
        logging.info("Добавление системного атрибута. Не указано тело запроса")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'system_attribute')
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Отправляем запрос
        response = profile_api.post("/profile/system-attributes/add",
                                    headers = headers)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'system_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        logging.debug(f"Кол-во записей в БД до - {count_record_before} и после - {count_record_after}")
        assert count_record_before == count_record_after, 'Кол-во записей в БД до и после не совпадает'
        
        logging.info(f"В БД ничего не добавилось.")
        logging.info(f"Тест завершен успешно.")
    
    ######################################################################################################################################
    
    @allure.epic("Добавление системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные системного атрибута')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52107")
    def test_c52107_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52107")
        logging.info("Добавление системного атрибута. Некорректные данные системного атрибута")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'system_attribute')
        
        body = {
            "display": system_attributes_wrong,
            "required": system_attributes_wrong,
            "name": f"{system_attributes_names_wrong}",
            "jsonName": f"{system_attributes_jsonNames_wrong}",
            "fieldOrder": system_attributes_wrong,
            "fieldType": system_attributes_wrong,
            "userType": f"{system_attributes_wrong}",
            "region": f"{system_attributes_wrong}",
            "metadata": system_attributes_wrong
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/system-attributes/add", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"name = '{system_attributes_names_wrong}'")
        
        with allure.step("Проверка того, что в БД нет записи"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД есть записи"
            logging.info(f"В БД нет записей.")
        
        params = {
            "jsonName": f"{system_attributes_jsonNames_wrong}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        parse_response_json(response)
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'system_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        logging.debug(f"Кол-во записей в БД до - {count_record_before} и после - {count_record_after}")
        assert count_record_before == count_record_after, 'Кол-во записей в БД до и после не совпадает'
        
        logging.info(f"В БД ничего не добавилось.")
        logging.info(f"Тест завершен успешно.")
    
    ######################################################################################################################################
    
    @allure.epic("Добавление системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные поля userType')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54677")
    def test_c54677_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54677")
        logging.info("Добавление системного атрибута. Некорректные данные поля userType")
        
        # Номер итерации для генерации данных
        i = 6
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'system_attribute')
        
        body = {
            "display": system_attributes_display_new[i],
            "required": system_attributes_required_new[i],
            "name": f"{system_attributes_name_new[i]}",
            "jsonName": f"{system_attributes_jsonName_new[i]}",
            "fieldOrder": system_attributes_fieldOrder_new[i],
            "fieldType": system_attributes_fieldType_new[i],
            "userType": f"{system_attributes_wrong}",
            "region": f"{system_attributes_region_new[i]}",
            "metadata": system_attributes_metadata_new[i]
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/system-attributes/add", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"json_name = '{system_attributes_jsonName_new[i]}'")
        
        with allure.step("Проверка того, что в БД нет записи"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД есть записи"
            logging.info(f"В БД нет записей.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        parse_response_json(response)
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'system_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        logging.debug(f"Кол-во записей в БД до - {count_record_before} и после - {count_record_after}")
        assert count_record_before == count_record_after, 'Кол-во записей в БД до и после не совпадает'
        
        logging.info(f"В БД ничего не добавилось.")
        logging.info(f"Тест завершен успешно.")
    
    ######################################################################################################################################
    
    @allure.epic("Добавление системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные поля region')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54678")
    def test_c54678_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54678")
        logging.info("Добавление системного атрибута. Некорректные данные поля region")
        
        # Номер итерации для генерации данных
        i = 6
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'system_attribute')
        
        body = {
            "display": system_attributes_display_new[i],
            "required": system_attributes_required_new[i],
            "name": f"{system_attributes_name_new[i]}",
            "jsonName": f"{system_attributes_jsonName_new[i]}",
            "fieldOrder": system_attributes_fieldOrder_new[i],
            "fieldType": system_attributes_fieldType_new[i],
            "userType": f"{system_attributes_userType_new[i]}",
            "region": f"{system_attributes_wrong}",
            "metadata": system_attributes_metadata_new[i]
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/system-attributes/add", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"json_name = '{system_attributes_jsonName_new[i]}'")
        
        with allure.step("Проверка того, что в БД нет записи"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД есть записи"
            logging.info(f"В БД нет записей.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        parse_response_json(response)
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'system_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        logging.debug(f"Кол-во записей в БД до - {count_record_before} и после - {count_record_after}")
        assert count_record_before == count_record_after, 'Кол-во записей в БД до и после не совпадает'
        
        logging.info(f"В БД ничего не добавилось.")
        logging.info(f"Тест завершен успешно.")
