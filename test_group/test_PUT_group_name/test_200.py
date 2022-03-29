import allure
import jmespath

from conftest import *
from functions import parse_request_json, parse_response_json, \
    assert_status_code, \
    params_record_db_condition, count_record_db_condition, gen_group


@allure.epic("Обновить группу")
@allure.description('Обновить группу')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test200:
    
    @allure.epic("Обновить группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52368")
    @pytest.mark.smoke
    def test_c52368_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52368")
        logging.info("Обновить группу. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызываем функцию создания группы
        gen_group(profile_api, i)
        
        # Номер итерации для обновления данных
        j = 3
        
        body = {
            "description": f"{group_gen_description}",
            "name": f"{group_gen_name[j]}"
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.put(
                f"group/{group_gen_name[i]}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Ниже берем новый name.
        # Получаем количество записей в БД по условию.
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_gen_name[j]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_gen_name[j]}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            list_len = len(param_ALL_group)  # считаем длину списка
            # Сверяем все строки из файла
            for y in range(list_len):
                json_value = jmespath.search(f"{param_ALL_group[y]}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_group[y], "attr_group",
                                                      f"name = '{group_gen_name[j]}' ORDER BY id ASC")
                
                assert f'{db_query}' == json_value, f"Параметр в БД {param_ALL_group[y]} = {db_query}.\n" \
                                                    f"Значение в json {param_ALL_group[y]} = {json_value}.\n"
        
        logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ##########################################################################################################################################
    
    @allure.epic("Обновить группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Указаны данные со старой информацией')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52373")
    def test_c52373_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52373")
        logging.info("Обновить группу. Указаны данные со старой информацией")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызываем функцию создания группы
        gen_group(profile_api, i)
        
        # Номер итерации для обновления данных
        j = 0
        
        body = {
            "description": f"{group_gen_description}",
            "name": f"{group_gen_name[j]}"
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.put(
                f"group/{group_gen_name[i]}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Ниже берем новый name.
        # Получаем количество записей в БД по условию.
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_gen_name[j]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_gen_name[j]}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            list_len = len(param_ALL_group)  # считаем длину списка
            # Сверяем все строки из файла
            for y in range(list_len):
                json_value = jmespath.search(f"{param_ALL_group[y]}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_group[y], "attr_group",
                                                      f"name = '{group_gen_name[j]}' ORDER BY id ASC")
                
                assert f'{db_query}' == json_value, f"Параметр в БД {param_ALL_group[y]} = {db_query}.\n" \
                                                    f"Значение в json {param_ALL_group[y]} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
            logging.info(f"Тест завершен успешно.")
