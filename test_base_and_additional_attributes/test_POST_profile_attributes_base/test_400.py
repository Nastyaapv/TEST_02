import allure

from conftest import *
from functions import count_record_db, count_record_db_condition, \
    parse_request_json, assert_status_code


@allure.epic("Добавить базовый атрибут")
@allure.description('Добавить базовый атрибут')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test400:
    
    @allure.epic("Добавить базовый атрибут")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52158")
    def test_c52158_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52158")
        logging.info("Добавить базовый атрибут. Не указано тело запроса")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'base_attribute')
        
        body = {
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("profile/attributes/base", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'base_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.debug(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################
    
    @allure.epic("Добавить базовый атрибут")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные базового атрибута')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52159")
    def test_c52159_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52159")
        logging.info("Добавить базовый атрибут. Некорректные данные базового атрибута")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'base_attribute')
        
        body = {
            "identity": f"{base_attribute_identity_wrong}",
            "name": f"{base_attribute_name_wrong}",
            "jsonName": f"{base_attribute_json_Name_wrong}",
            "type": base_attribute_type_wrong,
            "metadata": base_attribute_metadata_wrong
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("profile/attributes/base", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name = '{base_attribute_name_wrong}' and json_name = '{base_attribute_json_Name_wrong}'")
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД есть добавляемая запись "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД больше одной или вообще нет записей "
            logging.debug(f"В БД добавилась запись.")
        
        params = {
            "useJsonNameAsId": True
        }
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_json_Name_wrong}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'base_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.debug(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
