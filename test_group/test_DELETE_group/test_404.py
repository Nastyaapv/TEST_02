import allure

from conftest import *
from functions import assert_status_code, parse_response_json, count_record_db_condition, check_response_schema
from json_schemas import schema_404_error


@allure.epic("Удалить группу")
@allure.description('Удалить группу')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test404:
    
    @allure.epic("Удалить группу")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52375")
    def test_c52375_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52375")
        logging.info("Удалить группу. Несуществующий name")
        
        # Получаем количество записей в БД до выполнения запроса
        from functions import count_record_db
        count_record_before = count_record_db(dbCursor, 'attr_group')
        
        # Отправляем запрос
        response = profile_api.delete(
                f"group/{group_name_wrong}")  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'attr_group',
                                                 f"name = '{group_name_wrong}'")
        
        with allure.step("Проверяем количество необходимых записей в БД"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"Количество необходимых записей в БД больше нужного"
            
            # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name_wrong}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_after = count_record_db(dbCursor, 'attr_group')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса верное")
        logging.info(f"Тест завершен успешно.")
