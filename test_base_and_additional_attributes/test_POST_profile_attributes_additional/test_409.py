import allure
from functions import parse_request_json, check_response_schema, parse_response_json, assert_status_code, \
    count_record_db_condition, count_record_db

from conftest import *
from functions import gen_test_add_attribute_id
from json_schemas import schema_409_error


@allure.epic("Добавление дополнительных атрибутов получателей МГП")
@allure.description('Добавление дополнительных атрибутов получателей МГП')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test409:
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 409')
    @allure.story('Такой дополнительный атрибут уже существует по jsonName')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52177")
    def test_c52177_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52177")
        logging.info(
                "Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по jsonName")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызов функции генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, i)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Только jsonName должен повторяться
        body = {
            "display": additional_attribute_display_new[i + 2],
            "required": additional_attribute_required_new[i + 2],
            "name": f"{additional_attribute_name_new[i + 2]}",
            "jsonName": f"{additional_attribute_jsonName_new[i]}",
            "fieldOrder": additional_attribute_fieldOrder_new[i + 2],
            "fieldType": additional_attribute_fieldType_new[i + 2],
            "userType": f"{additional_attribute_userType_new[i + 2]}",
            "creationDate": f"{additional_attribute_creationDate_new[i + 2]}",
            "region": f"{additional_attribute_region_new[i + 2]}",
            "metadata": additional_attribute_metadata_new[i + 2]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_409_error)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 409)
        
        # Получаем количество записей в БД по условию
        count_new_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                     f"name = '{additional_attribute_name_new[i + 1]}' and json_name = '{additional_attribute_jsonName_new[i]}'")
        
        with allure.step("Проверка того, что в БД нет новой записи"):  # Записываем шаг в отчет allure
            assert count_new_record == 0, f"В БД больше 0 записей "
        
        # Получаем количество записей в БД по условию
        count_old_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                     f"json_name = '{additional_attribute_jsonName_new[i]}'")
        
        with allure.step("Проверка того, что в БД есть старая запись"):  # Записываем шаг в отчет allure
            assert count_old_record == 1, f"В БД больше одной или вообще нет записей "
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
