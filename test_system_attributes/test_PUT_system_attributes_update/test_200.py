import allure

from conftest import *
from functions import *


@allure.epic("Изменение системного атрибута")
@allure.description("Изменение системного атрибута")
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test200:
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52111")
    @pytest.mark.smoke
    def test_c52111_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52111")
        logging.info("Изменение системного атрибута. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызов функции генерации системного атрибута
        gen_system_attributes(profile_api, i)
        
        # Номер итерации для обновления данных
        j = 1
        
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
        
        # Получаем параметр в БД условию
        system_attributes_id = params_record_db_condition(dbCursor, "id", "system_attribute",
                                                          f"json_name = '{system_attributes_jsonName_new[i]}'")
        
        params = {
            "id": f"{system_attributes_id}",
            "useJsonNameAsId": False
        }
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params, headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"id = {system_attributes_id} and json_name = '{system_attributes_jsonName_new[i]}' and name = '{system_attributes_name_new[j]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                if key != 'display' and key != 'fieldOrder':
                    logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json[key]}")
                    
                    assert body[key] == response_json[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                            f"Значение в ответе метода {key} = {response_json[key]}.\n"
            logging.info(f"Значение JSON обновляемые и значения JSON сохраненные совпадают")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for y in range(count_record):  # цикл по содержимому БД
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    json_value = jmespath.search(f"{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key],
                                                          "system_attribute",
                                                          f"json_name = '{system_attributes_jsonName_new[i]}'")
                    
                    logging.debug(f"№ строки {y} - JSON param - {key} и значение  - {json_value}")
                    logging.debug(
                            f"№ строки {y} - БД param - {param_ALL_system_attribute[key]} и значение  - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    #####################################################################################################################################################
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 200')
    @allure.story('Использовать jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58395")
    def test_c58395_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58395")
        logging.info("Изменение системного атрибута. Использовать jsonName в качестве идентификатора")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции генерации системного атрибута
        gen_system_attributes(profile_api, i)
        
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
            "id": f"{system_attributes_jsonName_new[i]}",
            "useJsonNameAsId": True
        }
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params, headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"json_name = '{system_attributes_jsonName_new[i]}' and name = '{system_attributes_name_new[j]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                if key != 'display' and key != 'fieldOrder':
                    logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json[key]}")
                    
                    assert body[key] == response_json[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                            f"Значение в ответе метода {key} = {response_json[key]}.\n"
            logging.info(f"Значение JSON обновляемые и значения JSON сохраненные совпадают")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for y in range(count_record):  # цикл по содержимому БД
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    json_value = jmespath.search(f"{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key],
                                                          "system_attribute",
                                                          f"json_name = '{system_attributes_jsonName_new[i]}'")
                    
                    logging.debug(f"№ строки {y} - JSON param - {key} и значение  - {json_value}")
                    logging.debug(
                            f"№ строки {y} - БД param - {param_ALL_system_attribute[key]} и значение  - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ######################################################################################################################################################
    
    @allure.epic("Изменение системного атрибута")
    @allure.feature('Проверка кода 200')
    @allure.story('Указаны данные со старой информацией')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52118")
    def test_c52118_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52118")
        logging.info("Изменение системного атрибута. Указаны данные со старой информацией")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызов функции генерации системного атрибута
        gen_system_attributes(profile_api, i)
        
        # Номер итерации для обновления данных
        j = 1
        
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
        
        # Получаем параметр в БД условию
        system_attributes_id = params_record_db_condition(dbCursor, "id", "system_attribute",
                                                          f"json_name = '{system_attributes_jsonName_new[i]}'")
        
        params = {
            "id": f"{system_attributes_id}",
            "useJsonNameAsId": False
        }
        # Отправляем запрос
        response = profile_api.put(
                "profile/system-attributes/update", params = params, headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"id = {system_attributes_id} and json_name = '{system_attributes_jsonName_new[i]}' and name = '{system_attributes_name_new[j]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                if key != 'display' and key != 'fieldOrder':
                    logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json[key]}")
                    
                    assert body[key] == response_json[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                            f"Значение в ответе метода {key} = {response_json[key]}.\n"
            logging.info(f"Значение JSON обновляемые и значения JSON сохраненные совпадают")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for y in range(count_record):  # цикл по содержимому БД
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    json_value = jmespath.search(f"{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key],
                                                          "system_attribute",
                                                          f"json_name = '{system_attributes_jsonName_new[i]}'")
                    
                    logging.debug(f"№ строки {y} - JSON param - {key} и значение  - {json_value}")
                    logging.debug(
                            f"№ строки {y} - БД param - {param_ALL_system_attribute[key]} и значение  - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
