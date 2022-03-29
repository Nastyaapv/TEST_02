from functions import parse_request_json, parse_response_json, \
    assert_status_code, \
    count_record_db_condition

import allure

from conftest import *


@allure.epic("Обновить группу")
@allure.description('Обновить группу')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test404:
    
    @allure.epic("Обновить группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующий name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52369")
    def test_c52369_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52369")
        logging.info("Обновить группу. Несуществующий name")
        
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
                f"group/{group_name_wrong}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_name_wrong}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД есть записи "
            logging.info(f"В БД нет записей.")
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name_wrong}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        parse_response_json(response)
        
        logging.info(f"Тест завершен успешно.")
