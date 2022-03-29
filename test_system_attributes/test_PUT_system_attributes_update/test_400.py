import allure

from conftest import *
from functions import *


@allure.epic("Изменение системного атрибута")
@allure.description("Изменение системного атрибута")
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test400:
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52116")
    def test_c52116_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52116")
        logging.info("Изменение системного атрибута. Не указано тело запроса")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции генерации системного атрибута
        gen_system_attributes(profile_api, i)
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_before = parse_response_json(response)[0]
        
        headers = {
            "Content-Type": "application/json"
        }
        
        params = {
            "id": f"{system_attributes_jsonName_new[i]}",
            "useJsonNameAsId": True
        }
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params,
                headers = headers)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"json_name = '{system_attributes_jsonName_new[i]}'")
        
        with allure.step("Проверка того, что в БД нет записей"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД есть записи "
            logging.info(f"В БД нет записей.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_after = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия данных до выполнения запроса (response_json_before) и после (response_json_after)"):
            # Сверяем все строки json ответа
            for key in response_json_before:
                logging.debug(f"До выполнения запроса JSON параметр - {key} и значение  - {response_json_before[key]}")
                logging.debug(
                        f"После выполнения запроса JSON параметр - {key} и значение  - {response_json_after[key]}")
                
                assert response_json_before[key] == response_json_after[
                    key], f"Параметр в запросе на изменение {response_json_before[key]}.\n" \
                          f"Значение в ответе метода {key} = {response_json_after[key]}.\n"
            logging.info(f"Значения JSON до и после совпадают")
        
        logging.info(f"Тест завершен успешно.")
    
    #####################################################################################################################################################
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Пустое тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54681")
    def test_c54681_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54681")
        logging.info("Изменение системного атрибута. Пустое тело запроса")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции генерации системного атрибута
        gen_system_attributes(profile_api, i)
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_before = parse_response_json(response)[0]
        
        headers = {
            "Content-Type": "application/json"
        }
        
        body = {
        }
        
        params = {
            "id": f"{system_attributes_jsonName_new[i]}",
            "useJsonNameAsId": True
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params,
                headers = headers, data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"json_name = '{system_attributes_jsonName_new[i]}'")
        
        with allure.step("Проверка того, что в БД нет записей"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД есть записи "
            logging.info(f"В БД нет записей.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_after = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия данных до выполнения запроса (response_json_before) и после (response_json_after)"):
            # Сверяем все строки json ответа
            for key in response_json_before:
                logging.debug(f"До выполнения запроса JSON параметр - {key} и значение  - {response_json_before[key]}")
                logging.debug(
                        f"После выполнения запроса JSON параметр - {key} и значение  - {response_json_after[key]}")
                
                assert response_json_before[key] == response_json_after[
                    key], f"Параметр в запросе на изменение {response_json_before[key]}.\n" \
                          f"Значение в ответе метода {key} = {response_json_after[key]}.\n"
            logging.info(f"Значения JSON до и после совпадают")
        
        logging.info(f"Тест завершен успешно.")
    
    #####################################################################################################################################################
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные поля userType')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54683")
    def test_c54683_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54683")
        logging.info("Изменение системного атрибута. Некорректные данные поля userType")
        
        # Номер итерации для генерации данных
        i = 2
        
        # Вызов функции генерации системного атрибута
        gen_system_attributes(profile_api, i)
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_before = parse_response_json(response)[0]
        
        # Номер итерации для обновления данных
        j = 6
        
        body = {
            "required": system_attributes_required_new[j],
            "name": f"{system_attributes_name_new[j]}",
            "userType": system_attributes_id_wrong,
            "metadata": system_attributes_metadata_new[j]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        params = {
            "id": f"{system_attributes_jsonName_new[i]}",
            "useJsonNameAsId": True
        }
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params, headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"json_name = '{system_attributes_jsonName_new[i]}' and name = '{system_attributes_name_new[j]}'")
        
        with allure.step("Проверка того, что в БД нет записей"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД есть записи"
            logging.info(f"В БД нет записей.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_after = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия данных до выполнения запроса (response_json_before) и после (response_json_after)"):
            # Сверяем все строки json ответа
            for key in response_json_before:
                logging.debug(f"До выполнения запроса JSON параметр - {key} и значение  - {response_json_before[key]}")
                logging.debug(
                        f"После выполнения запроса JSON параметр - {key} и значение  - {response_json_after[key]}")
                
                assert response_json_before[key] == response_json_after[
                    key], f"Параметр в запросе на изменение {response_json_before[key]}.\n" \
                          f"Значение в ответе метода {key} = {response_json_after[key]}.\n"
            logging.info(f"Значения JSON до и после совпадают")
        
        logging.info(f"Тест завершен успешно.")
    
    #####################################################################################################################################################
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректный id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52117")
    def test_c52117_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52117")
        logging.info("Изменение системного атрибута. Некорректный id")
        
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
            "id": f"{invalid_symbol}",
            "useJsonNameAsId": False
        }
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params, headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Todo можно добавить еще какую-то сверку с гетом например, не обязательно
        
        logging.info(f"Тест завершен успешно.")
