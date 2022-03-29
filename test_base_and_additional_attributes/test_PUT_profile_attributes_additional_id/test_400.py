import allure
import jmespath

from conftest import *

from functions import parse_request_json, check_response_schema, parse_response_json, \
    assert_status_code, \
    reformatted_param, params_record_db_condition, gen_test_add_attribute_id

from json_schemas import GET_profile_attributes_additional_200_main_schema, schema_400_error


@allure.epic("Обновление данных дополнительного атрибута")
@allure.description("Обновление данных дополнительного атрибута")
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test400:
    
    @allure.epic("Обновление данных дополнительного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52188")
    def test_c52188_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52188")
        logging.info("Обновление данных дополнительного атрибута. Не указано тело запроса")
        
        # Номер итерации для генерации данных
        i = 4  # Сначала создаем атрибут или берем существующий
        
        # Вызов функции генерации дополнительного атрибута
        additional_attribute_id_new = gen_test_add_attribute_id(profile_api, dbCursor, i)[1]
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные потом не изменятся
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_new}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_before, response_json_beautifully = parse_response_json(response)
        
        # Отправляем запрос
        response = profile_api.put(
                f"/profile/attributes/additional/{additional_attribute_id_new}")
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_new}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json_after, response_json_beautifully = parse_response_json(response)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json_after,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка того, что после обновления данные не изменились:"):
            assert response_json_before == response_json_after, f'Данные до : {response_json_before}\n' \
                                                                f'Данные после : {response_json_after}'
            logging.info('Данные после неудачного обновления, не изменились!')
        logging.info('Тест завершен успешно!')
    
    ################################################################################################################################################################
    
    @allure.epic("Обновление данных дополнительного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Указаны не все поля в теле запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52677")
    def test_c52677_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52677")
        logging.info("Обновление данных дополнительного атрибута. Указаны не все поля в теле запроса")
        
        # Номер итерации для генерации данных additional_attribute_<param>_new
        i = 9  # Сначала создаем атрибут
        
        # Вызываем функцию генерации дополнительного атрибута
        additional_attribute_id_new = gen_test_add_attribute_id(profile_api, dbCursor, i)[1]
        
        with allure.step(
                f"Вызываем метод получение данных атрибута, для проверки того, что данные обновились"):  # Записываем шаг в отчет allure
            
            # Вызываем метод получения доп. атрибута для проверки того, что данные создались
            response = profile_api.get(
                    f"/profile/attributes/additional/{additional_attribute_id_new}")  # Записываем ответ метода GET в переменную response
            
            # Парсинг тела ответа
            response_json_before, response_json_beautifully = parse_response_json(response)  # Парсинг тела ответа
        
        # Номер итерации для генерации данных additional_attribute_<param>_new
        j = 10
        
        body = {
            "name": f"{additional_attribute_name_new[j]}",
            "userType": f"{additional_attribute_userType_new[j]}",
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.put(
                f"/profile/attributes/additional/{additional_attribute_id_new}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step(
                f"Вызываем метод получение данных атрибута, для проверки того, что данные обновились"):  # Записываем шаг в отчет allure
            
            # Вызываем метод получения доп. атрибута для проверки того, что данные создались
            response = profile_api.get(
                    f"/profile/attributes/additional/{additional_attribute_id_new}")  # Записываем ответ метода GET в переменную response
            
            # Парсинг тела ответа
            response_json_after, response_json_beautifully = parse_response_json(response)  # Парсинг тела ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json_after,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверяем, что данные обновились"):
            # Для проверки того, что значения в БД изменились.
            assert response_json_before != response_json_after, f'Данные до: {response_json_before}' \
                                                                f'Данные после: {response_json_after}'
            for key in body:
                logging.debug(f'Обновляемый ключ - {key}, значение - {body[key]}')
                logging.debug(f'Сохраненное ключ - {key}, значение - {response_json_after[key]}')
                assert body[key] == response_json_after[key], 'Сохраненные данные не соответствуют обновляемым.'
            logging.info(f'Сохраненные данные соответствуют обновляемым.')
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for key in param_ALL_additional_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json_after)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value)
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                      'additional_attribute',
                                                      f"id = {additional_attribute_id_new}")
                # Логирование, для отладки
                logging.debug(f"JSON-данные {json_value} - ключ {key}")
                logging.debug(f"БД-данные {db_query} - ключ БД {param_ALL_additional_attribute[key]}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Обновление данных дополнительного атрибута")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректный id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52189")
    def test_c52189_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52189")
        logging.info("Обновление данных дополнительного атрибута. Некорректный id")
        
        # Номер итерации для генерации данных
        j = 9
        
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
                f"/profile/attributes/additional/{additional_attribute_id_wrong_str}", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_400_error)  # Проверка JSON-схемы ответа
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_wrong_str}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_400_error)  # Проверка JSON-схемы ответа
        logging.info(f"Тест завершен успешно.")

####################################################################################################################################################################
