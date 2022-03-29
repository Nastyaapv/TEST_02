import allure

from conftest import *
from functions import parse_response_json, check_response_schema, \
    count_record_db_condition, count_record_db, assert_status_code
from json_schemas import schema_400_error


@allure.epic("Удалить дополнительный атрибут")
@allure.description('Удалить дополнительный атрибут')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test400:
    
    @allure.epic("Удалить дополнительный атрибут")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректный id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55355")
    def test_c55355_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55355")
        logging.info("Удалить дополнительный атрибут. Несуществующий id")
        
        # Получаем количество записей в БД
        count_record_db_before = count_record_db(dbCursor, 'additional_attribute')
        
        params = {
            "useJsonNameAsId": False
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/additional/{invalid_symbol}", params = params)
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_400_error)  # Проверка JSON-схемы ответа
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/additional/{invalid_symbol}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_400_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f" id = '{additional_attribute_id_wrong}'")
        # Получаем количество записей в БД
        count_record_db_after = count_record_db(dbCursor, 'additional_attribute')
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД нет записи "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД есть запись. "
            logging.debug(f"В БД не добавилась запись.")
        
        with allure.step("Проверка того, что в БД нет удаляемой записи"):  # Записываем шаг в отчет allure
            assert count_record_db_before == count_record_db_after, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД ничего не удалилось.")
        logging.info(f"Тест завершен успешно.")
