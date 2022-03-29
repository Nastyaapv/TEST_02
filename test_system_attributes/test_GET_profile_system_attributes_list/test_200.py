import allure
import jmespath

from conftest import *
from functions import gen_system_attributes, reformatted_param, params_record_db_condition, check_response_schema, \
    assert_status_code, parse_response_json, count_record_db_condition, count_record_db
from json_schemas import GET_profile_system_attributes_list_200_main_schema


@allure.epic("Получение существующих системных атрибутов")
@allure.description('Получение существующих системных атрибутов')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test200:
    
    @allure.epic("Получение существующих системных атрибутов")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий(Полное совпадение)')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/50506")
    @pytest.mark.smoke
    def test_c50506_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/50506")
        logging.info("Получение существующих системных атрибутов. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции генерации системного атрибута
        system_attributes_json_names, system_attributes_names = gen_system_attributes(profile_api, i)
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "system_attribute",
                                                    f"name like '%{system_attributes_names}%' or json_name like '%{system_attributes_json_names}%'")
        
        params = {
            "names": f"{system_attributes_names}",
            "jsonNames": f"{system_attributes_json_names}"
        }
        
        response = profile_api.get("/profile/system-attributes/list",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_system_attributes_list_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == 1, 'Кол-во записей json не равно 1'
        assert count_json == db_count_record, 'Кол-во записей в БД и json не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    r_id = jmespath.search(f"[{i}].id", response_json)  # получаем значение id
                    
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                          f"id = {r_id}")
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение существующих системных атрибутов")
    @allure.feature('Проверка кода 200')
    @allure.story('Частичное совпадение')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/53753")
    # Не дефект https://git.dev-mcx.ru/zenit/profile-service/-/issues/44
    def test_c53753_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/53753")
        logging.info("Получение существующих системных атрибутов. Частичное совпадение")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции генерации системного атрибута
        system_attributes_json_names, system_attributes_names = gen_system_attributes(profile_api, i)
        
        system_attributes_part_names = system_attributes_names[:7]
        system_attributes_part_json_names = system_attributes_json_names[:7]
        
        params = {"names": f"{system_attributes_part_names}",
                  "jsonNames": f"{system_attributes_part_json_names}"}
        
        response = profile_api.get("/profile/system-attributes/list",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_system_attributes_list_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "system_attribute",
                                                    f"name like '%{system_attributes_part_names}%' or json_name like '%{system_attributes_part_json_names}%'")
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == db_count_record, f"Количество подписей до выполнения запроса: {db_count_record}, после: {count_json}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    r_id = jmespath.search(f"[{i}].id", response_json)  # получаем значение id
                    
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                          f"id = {r_id}")
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение существующих системных атрибутов")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52099")
    def test_c52099_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52099")
        logging.info("Получение существующих системных атрибутов. Указан только jsonNames")
        
        # Номер итерации для генерации данных
        i = 1
        # Вызов функции генерации системного атрибута
        system_attributes_json_names = gen_system_attributes(profile_api, i)[0]
        
        # Указываем данные запроса
        params = {"jsonNames": f"{system_attributes_json_names}"}
        
        response = profile_api.get("/profile/system-attributes/list",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_system_attributes_list_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "system_attribute",
                                                    f"json_name = '{system_attributes_json_names}'")
        
        assert count_json == 1, 'Кол-во записей json не равно 1'
        assert count_json == db_count_record, 'Кол-во записей в БД и json не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                          f"json_name = '{system_attributes_json_names}'")
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение существующих системных атрибутов")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только Names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52098")
    def test_c52098_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52098")
        logging.info("Получение существующих системных атрибутов. Указан только jsonNames")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции генерации системного атрибута
        system_attributes_names = gen_system_attributes(profile_api, i)[1]
        
        # Указываем данные запроса
        params = {"names": f"{system_attributes_names}"}
        
        response = profile_api.get("/profile/system-attributes/list",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_system_attributes_list_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "system_attribute",
                                                    f"name = '{system_attributes_names}'")
        
        assert count_json == 1, 'Кол-во записей json не равно 1'
        assert count_json == db_count_record, 'Кол-во записей в БД и json не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                          f"name like '%{system_attributes_names}%'")
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение существующих системных атрибутов")
    @allure.feature('Проверка кода 200')
    @allure.story('Не указаны jsonNames и names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52100")
    def test_c52100_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52100")
        logging.info("Получение существующих системных атрибутов. Не указаны jsonNames и names")
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db(dbCursor, "system_attribute")
        
        response = profile_api.get(
                "/profile/system-attributes/list")  # Записываем ответ метода GET в переменную response
        
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_system_attributes_list_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json != 0, 'Кол-во записей json не равно 1'
        assert count_json == db_count_record, 'Кол-во записей в БД и json не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    r_id = jmespath.search(f"[{i}].id", response_json)  # получаем значение id
                    
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                          f"id = {r_id}")
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ########################################################################################################################
    
    @allure.epic("Получение существующих системных атрибутов")
    @allure.feature('Проверка кода 200')
    @allure.story('Некорректный jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52679")
    # Не дефект https://git.dev-mcx.ru/zenit/profile-service/-/issues/37
    def test_c52679_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52679")
        logging.info("Получение существующих системных атрибутов. Некорректный jsonNames")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Функция генерации системного атрибута
        system_attributes_json_names, system_attributes_names = gen_system_attributes(profile_api, i)
        
        # Указываем данные запроса
        params = {"names": f"{system_attributes_names}",
                  "jsonNames": f"{system_attributes_jsonNames_wrong}"}
        
        response = profile_api.get(
                f"/profile/system-attributes/list",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "system_attribute",
                                                    f"name like '%{system_attributes_names}%' or json_name like '%system_attributes_jsonNames_wrong%'")
        
        assert count_json != 0, 'Кол-во записей json - 0'
        assert count_json == db_count_record, 'Кол-во записей в БД и json не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                          f"name like '%{system_attributes_names}%' or json_name like '%system_attributes_jsonNames_wrong%'")
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ########################################################################################################################################
    
    @allure.epic("Получение существующих системных атрибутов")
    @allure.feature('Проверка кода 200')
    @allure.story('Некорректный names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52101")
    # Не дефект https://git.dev-mcx.ru/zenit/profile-service/-/issues/38
    def test_c52101_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52101")
        logging.info("Получение существующих системных атрибутов. Некорректный names")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции генерации системного атрибута
        system_attributes_json_names, system_attributes_names = gen_system_attributes(profile_api, i)
        
        # Указываем данные запроса
        params = {"names": f"{system_attributes_names_wrong}",
                  "jsonNames": f"{system_attributes_json_names}"}
        
        response = profile_api.get(
                f"/profile/system-attributes/list",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "system_attribute",
                                                    f"name like '%{system_attributes_names_wrong}%' or json_name like '%{system_attributes_json_names}%'")
        
        assert count_json != 0, 'Кол-во записей json равно 0'
        assert count_json == db_count_record, 'Кол-во записей в БД и json не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                          f"name like '%{system_attributes_names_wrong}%' or json_name like '%{system_attributes_json_names}%'")
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение существующих системных атрибутов")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующий names и jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55358")
    def test_c55358_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55358")
        logging.info("Получение существующих системных атрибутов. Несуществующий names и jsonNames")
        
        params = {"names": f"{system_attributes_names_wrong}",
                  "jsonNames": f"{system_attributes_jsonNames_wrong}"}
        
        response = profile_api.get("/profile/system-attributes/list",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_system_attributes_list_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Получаем параметр в БД условию
        db_count_record = count_record_db_condition(dbCursor, "system_attribute",
                                                    f"name like '%{system_attributes_names_wrong}%' or json_name like '%{system_attributes_jsonNames_wrong}%'")
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == 0, 'Кол-во записей не равно 0'
        assert count_json == db_count_record, 'Кол-во записей в БД и json не равно'
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == db_count_record, f"Количество подписей до выполнения запроса: {db_count_record}, после: {count_json}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                # Сверяем все строки из файла
                for key in param_ALL_system_attribute:
                    r_id = jmespath.search(f"[{i}].id", response_json)  # получаем значение id
                    
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_system_attribute[key], "system_attribute",
                                                          f"id = {r_id}")
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value)
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_system_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
