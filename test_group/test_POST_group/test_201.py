import allure

from conftest import *

import jmespath
from functions import parse_request_json, parse_response_json, \
    assert_status_code, params_record_db_condition, count_record_db_condition


@allure.epic("Создать группу")
@allure.description('Создать группу')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test201:
    
    @allure.epic("Создать группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52361")
    @pytest.mark.smoke
    def test_c52361_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52361")
        logging.info("Создать группу. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 2
        
        body = {
            "name": f"{group_gen_name[i]}",
            "description": f"{group_gen_description}",
            "role": f"{group_gen_role[i]}"
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post(
                "group", headers = headers, data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_gen_name[i]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД появилась новая запись.")
            
            # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_gen_name[i]}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            # Список параметров для сверки один, т.к. ключи БД и JSON одинаковые
            list_len = len(param_ALL_group)  # считаем длину списка
            # Сверяем все строки из файла
            for y in range(list_len):
                json_value = jmespath.search(f"{param_ALL_group[y]}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_group[y], "attr_group",
                                                      f"name = '{group_gen_name[i]}' ORDER BY id ASC")
                
                assert f'{db_query}' == json_value, f"Параметр в БД {param_ALL_group[y]} = {db_query}.\n" \
                                                    f"Значение в json {param_ALL_group[y]} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ###############################################################
    
    @allure.epic("Создать группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Разные типы ролей')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58126")
    @pytest.mark.parametrize('user_type', ['B', 'L', 'A', 'P'])
    def test_c58126_main(self, profile_api, cn, dbCursor, user_type):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58126")
        logging.info("Создать группу. Разные типы ролей")
        
        list_index = {'B': 5, 'L': 6, 'A': 7, 'P': 8}
        
        i = None  # Объявление переменной, что бы не ругался PEP 8
        
        if user_type in list_index:
            i = list_index[user_type]
        
        body = {
            "name": f"{group_gen_name[i]}",
            "description": f"{group_gen_description}",
            "role": f"{user_type}"
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post(
                "group", headers = headers, data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_gen_name[i]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД появилась новая запись.")
            
            # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_gen_name[i]}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            # Список параметров для сверки один, т.к. ключи БД и JSON одинаковые
            list_len = len(param_ALL_group)  # считаем длину списка
            # Сверяем все строки из файла
            for y in range(list_len):
                json_value = jmespath.search(f"{param_ALL_group[y]}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_group[y], "attr_group",
                                                      f"name = '{group_gen_name[i]}' ORDER BY id ASC")
                
                assert f'{db_query}' == json_value, f"Параметр в БД {param_ALL_group[y]} = {db_query}.\n" \
                                                    f"Значение в json {param_ALL_group[y]} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
