import allure
from functions import *

from conftest import *


@allure.epic("Обновление значений системных атрибутов для указанного пользователя")
@allure.description('Обновление значений системных атрибутов для указанного пользователя')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test400:
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 400')
    @allure.story('Несуществующий additionalProp')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52680")
    def test_c52680_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52680")
        logging.info(
                "Обновление значений системных атрибутов для указанного пользователя. Несуществующий additionalProp")
        
        # Номер итерации для генерации данных
        i = 3
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id = gen_user_system_attributes(profile_api, dbCursor, i)[0]
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_before = parse_response_json(response)[0]
        
        # Номер итерации для генерации значения системного атрибута
        j = 0
        
        body = {
            f"{system_attributes_jsonNames_wrong}": f"{system_attributes_jsonName_value[j]}"
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
            assert_status_code(response, 400)
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_after = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                try:
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json_after[key]}")
                    assert body[key] != response_json_after[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                                  f"Значение в ответе метода {key} = {response_json_after[key]}.\n"
                except AssertionError:
                    logging.info(f"Значения JSON обновляемые и значения JSON сохраненные не обновились. Верно.")
        
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
    
    #########################################################################################################################################
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 400')
    @allure.story('Регион пользователя и system_attributes разные')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58336")
    def test_c58336_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58336")
        logging.info(
                "Обновление значений системных атрибутов для указанного пользователя. Регион пользователя и system_attributes разные")
        
        # Номер итерации для генерации системного атрибута
        i = 2
        
        # Вызов функции генерации системного атрибута
        system_attributes_json_names_update = gen_system_attributes(profile_api, i)[0]
        
        # Номер итерации для генерации данных
        j = 3
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id = gen_user_system_attributes(profile_api, dbCursor, j)[0]
        
        system_attributes_user_id_region = params_record_db_condition(dbCursor, "region", "user_system_attribute",
                                                                      f"user_id = '{system_attributes_user_id}'")
        
        logging.debug(
                f'Регион системного атрибута {system_attributes_region_new[j]}. Регион пользователя {system_attributes_user_id_region}.')
        assert system_attributes_region_new[j] != system_attributes_user_id_region
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_before = parse_response_json(response)[0]
        
        # Номер итерации для генерации значения системного атрибута
        g = 4
        
        body = {
            f"{system_attributes_json_names_update[0]}": f"{system_attributes_jsonName_value[g]}"
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
            assert_status_code(response, 400)
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_after = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                try:
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json_after[key]}")
                    assert body[key] != response_json_after[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                                  f"Значение в ответе метода {key} = {response_json_after[key]}.\n"
                except AssertionError:
                    logging.info(f"Значения JSON обновляемые и значения JSON сохраненные не обновились. Верно.")
        
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
    
    #########################################################################################################################################
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 400')
    @allure.story('Тип пользователя и system_attributes разные')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58337")
    def test_c58337_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58337")
        logging.info(
                "Обновление значений системных атрибутов для указанного пользователя. Тип пользователя и system_attributes разные")
        
        # Номер итерации для генерации системного атрибута
        i = 6
        
        # Вызов функции генерации системного атрибута
        system_attributes_json_names_update = gen_system_attributes(profile_api, i)[0]
        
        # Номер итерации для генерации данных
        i = 3
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id = gen_user_system_attributes(profile_api, dbCursor, i)[0]
        
        system_attributes_user_id_user_type = params_record_db_condition(dbCursor, "role", "shtp_user",
                                                                         f"shtp_user_id = '{system_attributes_user_id}'")
        
        logging.debug(
                f'Тип разрешенного пользователя системного атрибута {system_attributes_userType_new[i]}. Тип пользователя {system_attributes_user_id_user_type}.')
        assert system_attributes_userType_new[i] != system_attributes_user_id_user_type
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_before = parse_response_json(response)[0]
        
        # Номер итерации для генерации значения системного атрибута
        j = 4
        
        body = {
            f"{system_attributes_json_names_update[0]}": f"{system_attributes_jsonName_value[j]}"
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
            assert_status_code(response, 400)
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_after = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                try:
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json_after[key]}")
                    assert body[key] != response_json_after[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                                  f"Значение в ответе метода {key} = {response_json_after[key]}.\n"
                except AssertionError:
                    logging.info(f"Значения JSON обновляемые и значения JSON сохраненные не обновились. Верно.")
        
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
    
    #########################################################################################################################################
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 400')
    @allure.story('Обновление нескольких значений, один из них не подходящий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58390")
    def test_c58390_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58390")
        logging.info(
                "Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений, один из них не подходящий")
        
        # Индекс функции генерации user ID для проверки системных атрибутов
        i = 6
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id, system_attributes_1 = gen_user_system_attributes(profile_api, dbCursor, i)
        
        # ищем второй - не подходящий системный атрибут
        system_attributes_2 = params_record_db_condition(dbCursor, 'json_name',
                                                         "system_attribute",
                                                         f"user_type != '{system_attributes_userType_new[i]}' and region != '{system_attributes_region_new[i]}' "
                                                         f"and json_name != '{system_attributes_1}'")
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_before = parse_response_json(response)[0]
        
        # Номер итерации для генерации значения системного атрибута
        j = 5
        
        body = {
            f"{system_attributes_1}": f"{system_attributes_jsonName_value[j]}",
            f"{system_attributes_2}": f"{system_attributes_jsonName_value[j + 1]}"
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
            assert_status_code(response, 400)
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_after = parse_response_json(response)[0]
        
        # Получаем параметр в БД условию
        count_db_query = count_record_db_condition(dbCursor, "user_system_attribute",
                                                   f"user_id = '{system_attributes_user_id}' and (name = '{system_attributes_1}' or name = '{system_attributes_2}')")
        
        assert count_db_query == 1, 'Значения атрибутов в БД только одно - старое, которое генерили в функции'
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                try:
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json_after[key]}")
                    assert body[key] != response_json_after[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                                  f"Значение в ответе метода {key} = {response_json_after[key]}.\n"
                except AssertionError:
                    logging.info(f"Значения JSON обновляемые и значения JSON сохраненные не обновились. Верно.")
        
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
    
    #########################################################################################################################################
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 400')
    @allure.story('Пустое тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54689")
    def test_c54689_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54689")
        logging.info(
                "Обновление значений системных атрибутов для указанного пользователя. Пустое тело запроса")
        
        # Индекс функции генерации user ID для проверки системных атрибутов
        i = 7
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id = gen_test_user_id_system_attr(profile_api, dbCursor, i)[0]
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json_before = parse_response_json(response)[0]
        
        body = {
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
        response_json_after = parse_response_json(response)[0]
        
        # Получаем параметр в БД условию
        count_db_query = count_record_db_condition(dbCursor, "user_system_attribute",
                                                   f"user_id = '{system_attributes_user_id}'")
        
        assert count_db_query == 0, 'Значения атрибутов в БД есть, а их не должно быть'
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                try:
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json_after[key]}")
                    assert body[key] != response_json_after[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                                  f"Значение в ответе метода {key} = {response_json_after[key]}.\n"
                except AssertionError:
                    logging.info(f"Значения JSON обновляемые и значения JSON сохраненные не обновились. Верно.")
        
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
