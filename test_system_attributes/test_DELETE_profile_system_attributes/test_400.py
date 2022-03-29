import allure

from conftest import *
from functions import assert_status_code, count_record_db


@allure.epic("Удаление системного атрибута")
@allure.description('Удаление системного атрибута')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test400:
    
    @allure.epic("Удаление системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указывать id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52144")
    def test_c52144_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52144")
        logging.info("Удаление системного атрибута. Не указывать id")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'system_attribute')
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/system-attributes/delete")
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_after = count_record_db(dbCursor, 'system_attribute')
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД кол-во записей не изменилось"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"В БД одна или больше записей "
            logging.info(f"В БД кол-во записей не изменилось")
        
        logging.info(f"Тест завершен успешно.")
    
    ###############################################################################
    
    @allure.epic("Удаление системного атрибута")
    @allure.feature('Проверка кода 404')
    @allure.story('Неуказанный jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58266")
    def test_c58266_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58266")
        logging.info("Удаление системного атрибута. Неуказанный jsonName в качестве идентификатора")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'system_attribute')
        
        params = {
            "useJsonNameAsId": True
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/system-attributes/delete",
                params = params)  # Записываем ответ метода в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_after = count_record_db(dbCursor, 'system_attribute')
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД кол-во записей не изменилось"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"В БД одна или больше записей "
            logging.info(f"В БД кол-во записей не изменилось")
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################################
    
    @allure.epic("Удаление системного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректный id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54680")
    def test_c54680_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54680")
        logging.info("Удаление системного атрибута. Некорректный id")
        
        params = {
            "id": invalid_symbol
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/system-attributes/delete",
                params = params)  # Записываем ответ метода в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        params = {
            "id": f"{invalid_symbol}"
        }
        response = profile_api.get("/profile/system-attributes/get",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        #  Не проверяем из-за ошибки psycopg2.errors.InvalidTextRepresentation: invalid input syntax for integer: "!@#$%^*()_:;?/>.<,"
        # # Получаем количество записей в БД по условию
        # # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        # count_record_db_cond = count_record_db_condition(dbCursor, 'system_attribute',
        #                                                  f"id = '{invalid_symbol}'")
        # # Проверяем наличие в БД по условию
        # with allure.step("Проверка того, что в БД нет записи "):  # Записываем шаг в отчет allure
        #     assert count_record_db_cond == 0, f"В БД одна или больше записей "
        #     logging.info(f"В БД нет записей.")
        logging.info(f"Тест завершен успешно.")
