import allure

from conftest import *
from json_schemas import schema_404_error
from functions import check_response_schema, parse_response_json, \
    assert_status_code, count_record_db_condition


@allure.epic("Получить список атрибутов входящих в группу")
@allure.description('Получить список атрибутов входящих в группу')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test404:
    
    @allure.epic("Получить список атрибутов входящих в группу")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52378")
    def test_c52378_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52378")
        logging.info("Получить список атрибутов входящих в группу. Несуществующий name")
        
        params = {"block": f"{group_gen_block}"}
        
        # Указываем данные запроса
        response = profile_api.get(
                f"/group/{group_name_wrong}/attributes",
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
            # Получаем количество записей в БД до выполнения запроса
            db_query = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_name_wrong}'")
            
            assert db_query == 0, f"Количество записей в БД - {db_query}.\n" \
                                  f"Ожидаемое количество записей в БД - 0.\n"
        
        logging.debug(f"Данных нет в БД. Кейс успешный.")
        logging.info(f"Тест завершен успешно.")
