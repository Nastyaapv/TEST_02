import allure

from conftest import *
from functions import parse_request_json, check_response_schema, parse_response_json, \
    assert_status_code
from json_schemas import schema_404_error


@allure.epic("Изменить базовый атрибут")
@allure.description("Изменить базовый атрибут")
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test404:
    
    @allure.epic("Изменить базовый атрибут")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52162")
    def test_c52162_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52162")
        logging.info("Изменить базовый атрибут. Несуществующий id")
        
        # Номер итерации для использования данных
        j = 5
        
        body = {
            "name": f"{base_attribute_name_new[j]}",
            "metadata": base_attribute_metadata_new[j],
            "deleted": base_attribute_deleted_new[j]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.put(
                f"/profile/attributes/base/{base_attribute_id_wrong}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        # Вызываем метод получения базового атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_id_wrong}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Изменить базовый атрибут")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55350")
    # Minor - https://git.dev-mcx.ru/zenit/profile-service/-/issues/183
    def test_c55350_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55350")
        logging.info("Изменить базовый атрибут. Несуществующий jsonName в качестве идентификатора")
        
        # Номер итерации для использования данных
        j = 5
        
        body = {
            "name": f"{base_attribute_name_new[j]}",
            "metadata": base_attribute_metadata_new[j],
            "deleted": base_attribute_deleted_new[j]
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
                f"/profile/attributes/base/{base_attribute_json_Name_wrong}", headers = headers,
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
        
        # Вызываем метод получения базового атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_json_Name_wrong}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        logging.info(f"Тест завершен успешно.")
