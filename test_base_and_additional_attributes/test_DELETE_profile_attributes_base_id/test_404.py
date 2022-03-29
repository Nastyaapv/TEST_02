import allure

from conftest import *
from functions import parse_response_json, check_response_schema, \
    count_record_db_condition, count_record_db, assert_status_code
from json_schemas import schema_404_error


@allure.epic("Удалить базовый атрибут")
@allure.description('Удалить базовый атрибут')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test404:
    
    @allure.epic("Удалить базовый атрибут")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54673")
    def test_c54673_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54673")
        logging.info("Удалить базовый атрибут. Несуществующий id")
        
        # Получаем количество записей в БД
        count_record_db_before = count_record_db(dbCursor, 'base_attribute')
        
        params = {
            "useJsonNameAsId": False
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/base/{base_attribute_id_wrong}", params = params)
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные удалились
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_id_wrong}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД
        count_record_db_after = count_record_db(dbCursor, 'base_attribute')
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f" id = {base_attribute_id_wrong}")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД есть добавляемая запись "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД удалилась запись.")
        
        with allure.step("Проверка того, что в БД есть добавляемая запись "):  # Записываем шаг в отчет allure
            assert count_record_db_before == count_record_db_after, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД не удалилось ничего.")
        logging.info(f"Тест завершен успешно.")
    
    ############################################################################################
    
    @allure.epic("Удалить базовый атрибут")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55353")
    def test_c55353_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55353")
        logging.info("Удалить базовый атрибут. Несуществующий jsonName в качестве идентификатора")
        
        # Получаем количество записей в БД
        count_record_db_before = count_record_db(dbCursor, 'base_attribute')
        
        params = {
            "useJsonNameAsId": True
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/base/{base_attribute_json_Name_wrong}", params = params)
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные удалились
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_json_Name_wrong}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД
        count_record_db_after = count_record_db(dbCursor, 'base_attribute')
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f" json_name = '{base_attribute_json_Name_wrong}'")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД есть добавляемая запись "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД удалилась запись.")
        
        with allure.step("Проверка того, что в БД есть добавляемая запись "):  # Записываем шаг в отчет allure
            assert count_record_db_before == count_record_db_after, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД не удалилось ничего.")
        logging.info(f"Тест завершен успешно.")
    
    ############################################################################################
    
    @allure.epic("Удалить базовый атрибут")
    @allure.feature('Проверка кода 404')
    @allure.story('Некорректный jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55354")
    def test_c55354_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55354")
        logging.info("Удалить базовый атрибут. Некорректный jsonName в качестве идентификатора")
        
        # Получаем количество записей в БД
        count_record_db_before = count_record_db(dbCursor, 'base_attribute')
        
        params = {
            "useJsonNameAsId": True
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/base/{invalid_symbol}", params = params)
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные удалились
        response = profile_api.get(
                f"/profile/attributes/base/{invalid_symbol}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД
        count_record_db_after = count_record_db(dbCursor, 'base_attribute')
        
        with allure.step("Проверка того, что в БД есть добавляемая запись "):  # Записываем шаг в отчет allure
            assert count_record_db_before == count_record_db_after, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД не удалилось ничего.")
        logging.info(f"Тест завершен успешно.")
