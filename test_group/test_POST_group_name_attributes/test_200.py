import allure
import jmespath

from conftest import *
from functions import parse_request_json, gen_test_base_attribute_id, parse_response_json, \
    assert_status_code, \
    params_record_db_condition, count_record_db_condition, gen_group, gen_test_add_attribute_id


@allure.epic("Добавить атрибуты в группу")
@allure.description('Добавить атрибуты в группу')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test200:
    
    @allure.epic("Добавить атрибуты в группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52380")
    @pytest.mark.smoke
    def test_c52380_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52380")
        logging.info("Добавить атрибуты в группу. Прямой сценарий - Добавление 1 атрибута")
        
        # Номер итерации для генерации данных group
        i = 0
        
        # Вызываем функцию создания группы
        group_name = gen_group(profile_api, i)
        
        # Номер итерации для генерации данных add_attribute
        add = 10
        
        # Вызываем функцию генерации дополнительного атрибута, для проверки добавления уже существующего атрибута
        group_gen_attr_name = gen_test_add_attribute_id(profile_api, dbCursor, add)[0]
        
        body = {
            "attributes": [
                {
                    "attrName": f"{group_gen_attr_name}",
                    "position": 0,
                    "block": f"{group_gen_block}"
                }
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post(
                f"/group/{group_name}/attributes", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Проверяем наличие в БД по name и attr_name
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД,  название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_name}' and attr_name = '{group_gen_attr_name}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        params = {
            "block": f"{group_gen_block}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}/attributes",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0  # задаем переменную для продвижения по списку содержимого в теле ответа
        while i < count_record:  # цикл по содержимому БД
            # Сверяем все строки из файла
            for key in param_ALL_group_link:
                json_value = jmespath.search(f"[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                logging.debug(f"% атрибута {i} - JSON param - {key} и value - {json_value}")
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_group_link[key],
                                                      "attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id",
                                                      f"name = '{group_name}' and attr_name = '{group_gen_attr_name}'")
                logging.debug(f"% атрибута {i} - ДБ param - {param_ALL_group_link[key]} и value - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert f'{db_query}' == f'{json_value}', f"Параметр в БД {param_ALL_group_link[key]} = {db_query}.\n" \
                                                         f"Значение в json {key} = {json_value}.\n"
            i = i + 1  # Увеличиваем счетчик
        logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    #########################################################################################
    
    @allure.epic("Добавить атрибуты в группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Добавление нескольких атрибутов')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58141")
    def test_c58141_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58141")
        logging.info("Добавить атрибуты в группу. Добавление нескольких атрибутов")
        
        # TODO Предположительно - системный атрибут нельзя добавлять уточнить
        # Номер итерации для генерации данных group
        i = 4
        
        # Вызываем функцию создания группы
        group_name = gen_group(profile_api, i)
        
        # Номер итерации для генерации данных add_attribute
        add = 11
        
        # Вызываем функцию генерации дополнительного атрибута, для проверки добавления уже существующего атрибута
        group_gen_attr_name_add = gen_test_add_attribute_id(profile_api, dbCursor, add)[0]
        
        # Номер итерации для генерации данных BASE_attribute
        base = 2
        
        # Вызываем функцию генерации баз атрибута, для проверки добавления уже существующего атрибута
        gen_test_base_attribute_id(profile_api, dbCursor, base)
        group_gen_attr_name_base = base_attribute_json_name_new[base]
        
        # # Номер итерации для генерации данных system_attribute
        # SYS = 4
        # # Вызываем функцию генерации баз атрибута, для проверки добавления уже существующего атрибута
        # gen_system_attributes(profile_api, SYS)
        # group_gen_attr_Name_system = system_attributes_Names_new[SYS]
        #
        body = {
            "attributes": [
                {
                    "attrName": f"{group_gen_attr_name_add}",
                    "position": 1,
                    "block": f"{group_gen_block}"
                },
                {
                    "attrName": f"{group_gen_attr_name_base}",
                    "position": 2,
                    "block": f"{group_gen_block}"
                },
                # {
                #     "attrName": f"{group_gen_attr_Name_system}",
                #     # "position": group_gen_position,
                #     "block": f"{group_gen_block}"
                # }
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post(
                f"/group/{group_name}/attributes", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Парсинг тела ответа
        # response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Проверяем наличие в БД по name и attr_name
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД,  название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_name}' and (attr_name IN ('{group_gen_attr_name_add}', '{group_gen_attr_name_base}'))")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 2, f"В БД больше двух или меньше двух записей "
            logging.info(f"В БД есть запись.")
        
        params = {
            "block": f"{group_gen_block}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}/attributes",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for y in range(count_record):  # цикл по содержимому БД
                json_attr_name = jmespath.search(f'[{y}].attrName', response_json)
                # Сверяем все строки из файла
                for key in param_ALL_group_link:
                    json_value = jmespath.search(f"[{y}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    logging.debug(f"% атрибута {y} - JSON param - {key} и value - {json_value}")
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_group_link[key],
                                                          "attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id",
                                                          f"name = '{group_name}' and attr_name = '{json_attr_name}'")
                    logging.debug(f"% атрибута {y} - ДБ param - {param_ALL_group_link[key]} и value - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert f'{db_query}' == f'{json_value}', f"Параметр в БД {param_ALL_group_link[key]} = {db_query}.\n" \
                                                             f"Значение в json {key} = {json_value}.\n"
                i = i + 1  # Увеличиваем счетчик
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
    
    #########################################################################################
    
    @allure.epic("Добавить атрибуты в группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Такие данные уже есть в системе')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52385")
    def test_c52385_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52385")
        logging.info("Добавить атрибуты в группу. Такие данные уже есть в системе")
        
        # Todo должна выходить - 409 статус, и ошибка, а сейчас 200, завести багу
        # Номер итерации для генерации данных group
        i = 0
        
        # Вызываем функцию создания группы
        group_name = gen_group(profile_api, i)
        
        # Номер итерации для генерации данных add_attribute
        add = 10
        
        # Вызываем функцию генерации дополнительного атрибута, для проверки добавления уже существующего атрибута
        group_gen_attr_name = gen_test_add_attribute_id(profile_api, dbCursor, add)[0]
        
        body = {
            "attributes": [
                {
                    "attrName": f"{group_gen_attr_name}",
                    # "position": group_gen_position,
                    "block": f"{group_gen_block}"
                }
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post(
                f"/group/{group_name}/attributes", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Проверяем наличие в БД по name и attr_name
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД,  название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_name}' and attr_name = '{group_gen_attr_name}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД есть запись.")
        
        params = {
            "block": f"{group_gen_block}"
        }
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}/attributes",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0  # задаем переменную для продвижения по списку содержимого в теле ответа
        while i < count_record:  # цикл по содержимому БД
            # Сверяем все строки из файла
            for key in param_ALL_group_link:
                json_value = jmespath.search(f"[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                logging.debug(f"% атрибута {i} - JSON param - {key} и value - {json_value}")
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_group_link[key],
                                                      "attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id",
                                                      f"name = '{group_name}' and attr_name = '{group_gen_attr_name}'")
                logging.debug(f"% атрибута {i} - ДБ param - {param_ALL_group_link[key]} и value - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert f'{db_query}' == f'{json_value}', f"Параметр в БД {param_ALL_group_link[key]} = {db_query}.\n" \
                                                         f"Значение в json {key} = {json_value}.\n"
            i = i + 1  # Увеличиваем счетчик
        logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
