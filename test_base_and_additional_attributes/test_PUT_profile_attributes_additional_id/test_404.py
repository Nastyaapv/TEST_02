import allure

from conftest import *
from functions import parse_request_json, check_response_schema, parse_response_json, \
    assert_status_code
from json_schemas import schema_404_error


@allure.epic("Обновление данных дополнительного атрибута")
@allure.description("Обновление данных дополнительного атрибута")
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test404:
    
    @allure.epic("Обновление данных дополнительного атрибута")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52186")
    def test_c52186_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52186")
        logging.info("Обновление данных дополнительного атрибута. Несуществующий id")
        
        # Номер итерации для использования данных
        j = 5
        
        body = {
            "display": additional_attribute_display_new[j],
            "required": additional_attribute_required_new[j],
            "name": f"{additional_attribute_name_new[j]}",
            "fieldOrder": additional_attribute_fieldOrder_new[j],
            "userType": f"{additional_attribute_userType_new[j]}",
            "metadata": additional_attribute_metadata_new[j]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.put(
                f"/profile/attributes/additional/{additional_attribute_id_wrong}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_wrong}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Обновление данных дополнительного атрибута")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55335")
    # Minor - https://git.dev-mcx.ru/zenit/profile-service/-/issues/183
    def test_c55336_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55336")
        logging.info("Обновление данных дополнительного атрибута. Несуществующий jsonName в качестве идентификатора")
        
        # Номер итерации для использования данных
        j = 5
        
        body = {
            "display": additional_attribute_display_new[j],
            "required": additional_attribute_required_new[j],
            "name": f"{additional_attribute_name_new[j]}",
            "fieldOrder": additional_attribute_fieldOrder_new[j],
            "userType": f"{additional_attribute_userType_new[j]}",
            "metadata": additional_attribute_metadata_new[j]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        params = {
            'useJsonNameAsId': True
        }
        # Отправляем запрос
        response = profile_api.put(
                f"/profile/attributes/additional/{additional_attribute_jsonNames_wrong}", headers = headers,
                params = params,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        params = {
            'useJsonNameAsId': True
        }
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_jsonNames_wrong}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        logging.info(f"Тест завершен успешно.")
