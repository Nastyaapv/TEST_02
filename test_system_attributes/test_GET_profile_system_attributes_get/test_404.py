import allure

from conftest import *
from functions import assert_status_code, parse_response_json, check_response_schema, count_record_db_condition
from json_schemas import schema_404_error


@allure.epic("Получение системного атрибута по идентификатору")
@allure.description('Получение системного атрибута по идентификатору')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test404:
    
    @allure.epic("Получение системного атрибута по идентификатору")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52134")
    def test_c52134_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52134")
        logging.info("Получение системного атрибута по идентификатору. Несуществующий id")
        
        # Указываем данные запроса
        params = {"id": f"{system_attributes_id_int_wrong}"}
        
        response = profile_api.get(f"/profile/system-attributes/get",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что данных нет в БД"):
            # Получаем количество записей в БД по условию
            count_record_db_cond = count_record_db_condition(dbCursor, 'system_attribute',
                                                             f"id = {system_attributes_id_int_wrong}")
            
            assert count_record_db_cond == 0, f"Количество записей в БД - {count_record_db_cond}.\n" \
                                              f"Ожидаемое количество записей в БД - 0.\n"
        
        logging.debug(f"Данных нет в БД.")
        logging.info(f"Тест завершен успешно.")
