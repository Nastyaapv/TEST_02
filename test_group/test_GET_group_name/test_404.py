import allure

from conftest import *
from functions import parse_response_json, assert_status_code, check_response_schema, count_record_db_condition
from json_schemas import schema_404_error


@allure.epic("Получить данные о группе")
@allure.description('Получить данные о группе')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test404:
    
    @allure.epic("Получить данные о группе")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52393")
    # https://git.dev-mcx.ru/zenit/profile-service/-/issues/48 - ИСПРАВИЛИ
    def test_c52393_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52393")
        logging.info("Получить данные о группе. Несуществующий name")
        
        # Указываем данные запроса
        response = profile_api.get(
                f"/group/{group_name_wrong}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что данных нет в БД"):
            # Получаем количество записей в БД
            db_query = count_record_db_condition(dbCursor, 'attr_group', f"name = '{group_name_wrong}'")
            
            assert db_query == 0, f"Количество записей в БД - {db_query}.\n" \
                                  f"Ожидаемое количество записей в БД - 0.\n"
        
        logging.info(f"Данных нет в БД. Кейс успешный.")
        logging.info(f"Тест завершен успешно.")
