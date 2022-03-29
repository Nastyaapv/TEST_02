import allure

from conftest import *
from functions import parse_response_json, assert_status_code, count_record_db_condition, check_response_schema
from json_schemas import schema_404_error


@allure.epic("Получение значений системных атрибутов для указанного пользователя")
@allure.description('Получение значений системных атрибутов для указанного пользователя')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test404:
    
    @allure.epic("Получение значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий userId')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52197")
    def test_c52197_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52197")
        logging.info("Получение значений системных атрибутов для указанного пользователя. Несуществующий userId")
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_userId_wrong}/get")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
            
            # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "user_system_attribute",
                                                    f"user_id = '{system_attributes_userId_wrong}'")
        
        assert db_count_record == 0, 'В БД есть записи для этого пользователя'
        logging.info(f"Тест завершен успешно.")
