import allure

from conftest import *
from functions import parse_response_json, check_response_schema, \
    count_record_db, assert_status_code
from json_schemas import schema_405_error


@allure.epic("Удалить дополнительный атрибут")
@allure.description('Удалить дополнительный атрибут')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test405:
    
    @allure.epic("Удалить дополнительный атрибут")
    @allure.feature('Проверка кода 405')
    @allure.story('Не указывать id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52194")
    def test_c52194_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52194")
        logging.info("Удалить дополнительный атрибут. Не указывать id")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/additional/")
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 405)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_405_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.debug(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
