import allure
import jmespath

from conftest import *
from functions import assert_status_code, count_record_db_condition, reformatted_param, params_record_db_condition, \
    parse_response_json


@allure.epic("Добавление системного атрибута")
@allure.description('Добавление системного атрибута')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test201:
    
    @allure.epic("Добавление системного атрибута")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52102")
    @pytest.mark.smoke
    def test_c52102_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52102")
        logging.info("Добавление системного атрибута. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 3
        
        body = {
            "display": system_attributes_display_new[i],
            "required": system_attributes_required_new[i],
            "name": f"{system_attributes_name_new[i]}",
            "jsonName": f"{system_attributes_jsonName_new[i]}",
            "fieldOrder": system_attributes_fieldOrder_new[i],
            "fieldType": f"{system_attributes_fieldType_new[i]}",
            "userType": f"{system_attributes_userType_new[i]}",
            "region": f"{system_attributes_region_new[i]}",
            "metadata": system_attributes_metadata_new[i]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        from functions import parse_request_json
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/system-attributes/add", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'system_attribute',
                                                 f"name = '{system_attributes_name_new[i]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        params = {
            "jsonName": f"{system_attributes_jsonName_new[i]}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/profile/system-attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step(
                "Проверка соответствия обновляемых данных (body_json) и сохранившихся данных (response_json)"):
            # Сверяем все строки json ответа
            for key in body:
                if key != 'display' and key != 'fieldOrder':
                    logging.debug(f"JSON обновляемое - {key} и значение  - {body[key]}")
                    logging.debug(f"JSON сохраненное - {key} и значение  - {response_json[key]}")
                    
                    assert body[key] == response_json[key], f"Параметр в запросе на изменение {body[key]}.\n" \
                                                            f"Значение в ответе метода {key} = {response_json[key]}.\n"
            logging.info(f"Значение JSON обновляемые и значения JSON сохраненные совпадают")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for y in range(count_record):  # цикл по содержимому БД
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    json_value = jmespath.search(f"{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key],
                                                          "system_attribute",
                                                          f"json_name = '{system_attributes_jsonName_new[i]}'")
                    
                    logging.debug(f"№ строки {y} - JSON param - {key} и значение  - {json_value}")
                    logging.debug(
                            f"№ строки {y} - БД param - {param_ALL_system_attribute[key]} и значение  - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
