import allure

from functions import *
from conftest import *


@allure.epic("Обновление значений системных атрибутов для указанного пользователя")
@allure.description('Обновление значений системных атрибутов для указанного пользователя')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test200:
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52200")
    @pytest.mark.smoke
    def test_c52200_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52200")
        logging.info("Обновление значений системных атрибутов для указанного пользователя. Прямой сценарий")
        
        # Todo Написать инструкцию по заполнению этого метода по переписке с М. Ширшовым. Плюс, данные добавляются в таблицу указанного пользователя только этим методом соблюдением региона пользователя, типа пользователя.
        
        # Номер итерации для генерации данных
        i = 3
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id, system_attributes_json_names_update = gen_user_system_attributes(profile_api,
                                                                                                    dbCursor,
                                                                                                    i)
        # Номер итерации для генерации значения системного атрибута
        j = 4
        
        body = {
            f"{system_attributes_json_names_update}": f"{system_attributes_jsonName_value[j]}"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        response = profile_api.put(
                f"profile/system-attributes/user/{system_attributes_user_id}/set", headers = headers,
                data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                logging.debug(f"JSON сохраненное - {key} и значение  - {response_json[key]}")
                
                assert body[key] == response_json[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                        f"Значение в ответе метода {key} = {response_json[key]}.\n"
            logging.info(f"Значения JSON обновляемые и значения JSON сохраненные совпадают")
            
            with allure.step("Проверка что отобразились именно необходимые данные"):
                # Сверяем все строки из файла
                json_value = jmespath.search(f"{system_attributes_json_names_update}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_user_system_attribute,
                                                      "user_system_attribute",
                                                      f"user_id = '{system_attributes_user_id}' and name = '{system_attributes_json_names_update}'")
                
                logging.debug(f"Параметр в БД {param_ALL_user_system_attribute} = {db_query}.")
                logging.debug(f"Значение в json {param_ALL_user_system_attribute} = {json_value}.")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_user_system_attribute} = {db_query}.\n" \
                                               f"Значение в json {param_ALL_user_system_attribute} = {json_value}.\n"
                
                logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
            logging.info(f"Тест завершен успешно.")
    
    #########################################################################################################################################
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 200')
    @allure.story('Обновление нескольких значений')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58338")
    def test_c58338_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58338")
        logging.info(
                "Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений")
        
        # Кол-во атрибутов, которые будем добавлять пользователю
        counter = 2
        
        # Индекс функции генерации user ID для проверки системных атрибутов
        i = 4
        
        # Вызываем функцию генерации user ID для проверки системных атрибутов
        user_id = gen_test_user_id_system_attr(profile_api, dbCursor, i)[0]
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id, system_attributes_json_names_update = gen_many_user_system_attributes(profile_api,
                                                                                                         dbCursor,
                                                                                                         i, user_id,
                                                                                                         counter)
        
        # Номер итерации для генерации значения системного атрибута
        j = 5
        
        body = {
            f"{system_attributes_json_names_update[0]}": f'{system_attributes_jsonName_value[j]}',
            f"{system_attributes_json_names_update[1]}": f"{system_attributes_jsonName_value[j + 1]}",
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        response = profile_api.put(
                f"profile/system-attributes/user/{system_attributes_user_id}/set", headers = headers,
                data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Получаем параметр в БД условию
        count_db_query = count_record_db_condition(dbCursor, "user_system_attribute",
                                                   f"user_id = '{system_attributes_user_id}'")
        
        assert count_db_query == 2, 'Атрибутов в БД нет, или неправильное кол-во'
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                logging.debug(f"JSON сохраненное - {key} и значение  - {response_json[key]}")
                
                assert body[key] == response_json[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                        f"Значение в ответе метода {key} = {response_json[key]}.\n"
            logging.info(f"Значения JSON обновляемые и значения JSON сохраненные совпадают")
            
            with allure.step("Проверка что отобразились именно необходимые данные"):
                for y in range(counter):
                    # Сверяем все строки из файла
                    json_value = jmespath.search(f"{system_attributes_json_names_update[y]}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_user_system_attribute,
                                                          "user_system_attribute",
                                                          f"user_id = '{system_attributes_user_id}' and name = '{system_attributes_json_names_update[y]}'")
                    
                    logging.debug(f"Параметр в БД {param_ALL_user_system_attribute} = {db_query}.")
                    logging.debug(f"Значение в json {param_ALL_user_system_attribute} = {json_value}.")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_user_system_attribute} = {db_query}.\n" \
                                                   f"Значение в json {param_ALL_user_system_attribute} = {json_value}.\n"
                
                logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
            logging.info(f"Тест завершен успешно.")
    
    #############################################################################################################################
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 200')
    @allure.story('Указаны данные со старой информацией')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52205")
    def test_c52205_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52205")
        logging.info(
                "Обновление значений системных атрибутов для указанного пользователя. Указаны данные со старой информацией")
        
        # Номер итерации для генерации данных
        i = 3
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id, system_attributes_json_names_update = gen_user_system_attributes(profile_api,
                                                                                                    dbCursor,
                                                                                                    i)
        # Номер итерации для генерации значения системного атрибута
        j = 4
        
        body = {
            f"{system_attributes_json_names_update}": f"{system_attributes_jsonName_value[j]}"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        response = profile_api.put(
                f"profile/system-attributes/user/{system_attributes_user_id}/set", headers = headers,
                data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                logging.debug(f"JSON сохраненное - {key} и значение  - {response_json[key]}")
                
                assert body[key] == response_json[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                        f"Значение в ответе метода {key} = {response_json[key]}.\n"
            logging.info(f"Значения JSON обновляемые и значения JSON сохраненные совпадают")
            
            with allure.step("Проверка что отобразились именно необходимые данные"):
                # Сверяем все строки из файла
                json_value = jmespath.search(f"{system_attributes_json_names_update}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_user_system_attribute,
                                                      "user_system_attribute",
                                                      f"user_id = '{system_attributes_user_id}' and name = '{system_attributes_json_names_update}'")
                
                logging.debug(f"Параметр в БД {param_ALL_user_system_attribute} = {db_query}.")
                logging.debug(f"Значение в json {param_ALL_user_system_attribute} = {json_value}.")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_user_system_attribute} = {db_query}.\n" \
                                               f"Значение в json {param_ALL_user_system_attribute} = {json_value}.\n"
                
                logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
            logging.info(f"Тест завершен успешно.")
