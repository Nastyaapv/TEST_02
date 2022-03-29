from functions import parse_request_json, parse_response_json, \
    assert_status_code, count_record_db_condition, gen_group

import allure

from conftest import *


@allure.epic("Обновить группу")
@allure.description('Обновить группу')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test400:
    
    @allure.epic("Обновить группу")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52371")
    def test_c52371_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52371")
        logging.info("Обновить группу. Не указано тело запроса")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызываем функцию создания группы
        group_name = gen_group(profile_api, i)
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_before, response_json_beautifully = parse_response_json(response)
        
        body = {
        
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.put(
                f"group/{group_name}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_name}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
            
            # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_after, response_json_beautifully = parse_response_json(response)
        
        assert response_json_before == response_json_after, 'Данные не обновились'
        
        logging.info(f"Тест завершен успешно.")
    
    #######################################################################################################################
    
    @allure.epic("Обновить группу")
    @allure.feature('Проверка кода 400')
    @allure.story('Невалидный name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52372")
    def test_c52372_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52372")
        logging.info("Обновить группу. Невалидный name")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызываем функцию создания группы
        group_name = gen_group(profile_api, i)
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_before, response_json_beautifully = parse_response_json(response)
        
        body = {
            "description": f"{group_gen_description}",
            "name": f"{invalid_symbol}"
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.put(
                f"group/{group_name}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_name}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
            
            # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_after, response_json_beautifully = parse_response_json(response)
        
        assert response_json_before == response_json_after, 'Данные не обновились'
        
        logging.info(f"Тест завершен успешно.")
