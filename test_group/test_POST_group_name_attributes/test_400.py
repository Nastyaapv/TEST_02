import allure

from conftest import *
from functions import parse_request_json, parse_response_json, \
    assert_status_code, count_record_db_condition, gen_group


@allure.epic("Добавить атрибуты в группу")
@allure.description('Добавить атрибуты в группу')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test400:
    
    @allure.epic("Добавить атрибуты в группу")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52383")
    def test_c52383_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52383")
        logging.info("Добавить атрибуты в группу. Не указано тело запроса")
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Указываем данные запроса
        response = profile_api.post(
                f"/group/{group_name_wrong}/attributes",
                headers = headers)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        with allure.step("Проверка что данных нет в БД"):
            # Получаем количество записей в БД по условию
            count_record_db = count_record_db_condition(dbCursor,
                                                        'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                        f"name = '{group_name_wrong}'")
            
            assert count_record_db == 0, f"Количество записей в БД - {count_record_db}.\n" \
                                         f"Ожидаемое количество записей в БД - 0.\n"
        
        logging.info(f"Данных нет в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ##########################################################################################
    
    @allure.epic("Добавить атрибуты в группу")
    @allure.feature('Проверка кода 400')
    @allure.story('Указаны не все поля в теле запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/56110")
    def test_c56110_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/56110")
        logging.info("Добавить атрибуты в группу. Указаны не все поля в теле запроса")
        
        # Номер итерации для генерации данных group
        i = 5
        
        # Вызываем функцию создания группы
        group_name = gen_group(profile_api, i)
        
        body = {
            "attributes": [
                {
                    # "attrName": f"{group_gen_attr_Name}",
                    "position": 0,
                    "block": f"{group_gen_block}"
                }
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post(
                f"/group/{group_name}/attributes", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Проверяем наличие в БД по name и attr_name
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД,  название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_name}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        params = {
            "block": f"{group_gen_block}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}/attributes",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        parse_response_json(response)
        
        logging.info(f"Тест завершен успешно.")
