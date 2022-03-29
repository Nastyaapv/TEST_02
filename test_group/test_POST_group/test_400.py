import allure

from conftest import *
from functions import parse_request_json, parse_response_json, \
    assert_status_code, count_record_db_condition, count_record_db


@allure.epic("Создать группу")
@allure.description('Создать группу')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test400:
    
    @allure.epic("Создать группу")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52365")
    def test_c52365_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52365")
        logging.info("Создать группу. Не указано тело запроса")
        
        # Получаем количество записей в БД по условию
        count_record_before = count_record_db(dbCursor, 'attr_group')
        
        body = {
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
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        count_record_after = count_record_db(dbCursor, 'attr_group')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.debug(f"Количество записей в БД после выполнения запроса не изменилось")
        
        logging.info(f"Тест завершен успешно.")
    
    ######################################################################################################################
    
    @allure.epic("Создать группу")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные группы атрибутов')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52366")
    def test_c52366_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52366")
        logging.info("Создать группу. Некорректные данные группы атрибутов")
        
        # Номер итерации для генерации данных
        i = 4
        
        body = {
            "name": f"{group_gen_name[i]}",
            "description": f"{group_gen_description}",
            "role": f"{group_role_wrong}"
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
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_gen_name[i]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД появилась новая запись.")
            
            # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_gen_name[i]}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        parse_response_json(response)
        
        logging.info(f"Тест завершен успешно.")
