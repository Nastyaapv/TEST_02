import allure
import jmespath

from conftest import *
from functions import gen_system_attributes, params_record_db_condition, parse_response_json, assert_status_code, \
    reformatted_param, check_response_schema
from json_schemas import GET_profile_system_attributes_get_200_main_schema


@allure.epic("Получение системного атрибута по идентификатору")
@allure.description('Получение системного атрибута по идентификатору')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test200:
    
    @allure.epic("Получение системного атрибута по идентификатору")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52133")
    @pytest.mark.smoke
    def test_c52133_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52133")
        logging.info("Получение системного атрибута по идентификатору. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции генерации системного атрибута
        system_attributes_json_names = gen_system_attributes(profile_api, i)[0]
        
        # Получаем параметр в БД условию
        system_attributes_id = params_record_db_condition(dbCursor, "id", "system_attribute",
                                                          f"json_name = '{system_attributes_json_names}'")
        params = {
            "id": f"{system_attributes_id}"
        }
        
        response = profile_api.get("/profile/system-attributes/get",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_system_attributes_get_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            # Сверяем все строки из файла
            for key in param_ALL_system_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                      f"id = {system_attributes_id}")
                
                # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                json_value = reformatted_param(key, json_value)
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")

################################################################################################################################################################
