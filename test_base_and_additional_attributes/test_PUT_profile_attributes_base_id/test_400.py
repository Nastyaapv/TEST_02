import allure

from conftest import *
from functions import *
from json_schemas import schema_400_error, \
    GET_profile_attributes_base_id_200_main_schema


@allure.epic("Изменить базовый атрибут")
@allure.description("Изменить базовый атрибут")
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test400:
    
    @allure.epic("Изменить базовый атрибут")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52164")
    def test_c52164_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52164")
        logging.info("Изменить базовый атрибут. Не указано тело запроса")
        
        # Номер итерации для генерации данных
        i = 8  # Сначала создаем атрибут или берем существующий
        
        # Вызов функции генерации базового атрибута
        base_attribute_id = gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Вызываем метод получения базового атрибута для проверки того, что данные потом не изменятся
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_id}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_before, response_json_beautifully = parse_response_json(response)
        
        # Отправляем запрос
        response = profile_api.put(
                f"/profile/attributes/base/{base_attribute_id}")
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Вызываем метод получения базового атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_id}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_after, response_json_beautifully = parse_response_json(response)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json_after,
                                  GET_profile_attributes_base_id_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка того, что после обновления данные не изменились:"):
            assert response_json_before == response_json_after, f'Данные до : {response_json_before}\n' \
                                                                f'Данные после : {response_json_after}'
            logging.info('Данные после неудачного обновления, не изменились!')
        logging.info('Тест завершен успешно!')
    
    ################################################################################################################################################################
    
    @allure.epic("Изменить базовый атрибут")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректный id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52165")
    def test_c52165_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52165")
        logging.info("Изменить базовый атрибут. Некорректный id")
        
        # Номер итерации для генерации данных
        j = 7
        
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
                f"/profile/attributes/base/{base_attribute_id_wrong_str}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_400_error)  # Проверка JSON-схемы ответа
        
        # Вызываем метод получения базового атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_id_wrong_str}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_400_error)  # Проверка JSON-схемы ответа
        logging.info(f"Тест завершен успешно.")

####################################################################################################################################################################
