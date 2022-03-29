import allure

from conftest import *

import jmespath
from functions import parse_request_json, parse_response_json, \
    assert_status_code, params_record_db_condition, count_record_db_condition


@allure.epic("Создать группу")
@allure.description('Создать группу')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test409:
    
    @allure.epic("Создать группу")
    @allure.feature('Проверка кода 409')
    @allure.story('Такая группа атрибутов уже существует по name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52362")
    def test_c52362_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52362")
        logging.info("Создать группу. Такая группа атрибутов уже существует по name")
        
        # Номер итерации для генерации данных
        i = 2
        
        body = {
            "name": f"{group_gen_name[i]}",
            "description": f"{group_gen_description}",
            "role": f"{group_gen_role[i + 1]}"
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
            assert_status_code(response, 409)
        
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
