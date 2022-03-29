import allure

from conftest import *
from functions import *


@allure.epic("Обновление значений системных атрибутов для указанного пользователя")
@allure.description('Обновление значений системных атрибутов для указанного пользователя')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test404:
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий userId')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52201")
    def test_c52201_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52201")
        logging.info("Обновление значений системных атрибутов для указанного пользователя. Несуществующий userId")
        
        # Номер итерации для генерации данных
        i = 3
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id, system_attributes_json_names_update = gen_user_system_attributes(profile_api,
                                                                                                    dbCursor,
                                                                                                    i)
        # Номер итерации для генерации значения системного атрибута
        j = 1
        
        body = {
            f"{system_attributes_json_names_update}": f"{system_attributes_jsonName_value[j]}"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        response = profile_api.put(
                f"profile/system-attributes/user/{system_attributes_userId_wrong}/set", headers = headers,
                data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
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
                
                assert body[key] != response_json[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                        f"Значение в ответе метода {key} = {response_json[key]}.\n"
            logging.info(f"Значения JSON обновляемые и значения JSON сохраненные не обновились. Верно.")
            
            # Получаем параметр в БД условию
            db_count_record = count_record_db_condition(dbCursor, "user_system_attribute",
                                                        f"user_id = '{system_attributes_userId_wrong}' and name = '{system_attributes_json_names_update}'")
            assert db_count_record == 0, 'Данные пользователя о сист. атрибуте есть в БД'
            
            logging.info('Данных пользователя о сист. атрибуте нет в БД. Верно')
            logging.info(f"Тест завершен успешно.")
    
    ###############################################################################################################################################
    
    @allure.epic("Обновление значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 404')
    @allure.story('Невалидный userId')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52204")
    def test_c52204_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52204")
        logging.info("Обновление значений системных атрибутов для указанного пользователя. Невалидный userId")
        
        # ищем второй - не подходящий системный атрибут
        system_attribute = params_record_db_without_condition(dbCursor, 'json_name',
                                                              "system_attribute")
        
        # Номер итерации для генерации значения системного атрибута
        j = 1
        
        body = {
            f"{system_attribute}": f"{system_attributes_jsonName_value[j]}"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        response = profile_api.put(
                f"profile/system-attributes/user/{invalid_symbol}/set", headers = headers,
                data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        response = profile_api.get(
                f"profile/system-attributes/user/{invalid_symbol}/get")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Парсинг тела ответа
        parse_response_json(response)
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "user_system_attribute",
                                                    f"user_id = '{invalid_symbol}'")
        assert db_count_record == 0, 'Данные пользователя о сист. атрибуте есть в БД'
        
        logging.info('Данных пользователя о сист. атрибуте нет в БД. Верно')
        logging.info(f"Тест завершен успешно.")
