import allure
import jmespath

from conftest import *
from functions import parse_request_json, check_response_schema, parse_response_json, assert_status_code, \
    reformatted_param, params_record_db_condition, count_record_db_condition, count_record_db, \
    gen_test_add_attribute_id, record_size_pages, check_param_schema, sort_list

from json_schemas import GET_profile_attributes_additional_search_200_main_schema


@allure.epic("Получение списка дополнительных атрибутов (POST)")
@allure.description('Получение списка дополнительных атрибутов (POST)')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test200:
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий (полное совпадение)')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55269")
    @pytest.mark.smoke
    def test_c55269_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55269")
        logging.info("Получение списка дополнительных атрибутов (POST). Прямой сценарий (полное совпадение)")
        
        # Todo подумать над совершенствованием полной проверки ответа метода
        # Тут полное совпадение значит запись только одна будет
        
        j = 5  # Для списка additional_attribute_<param>_new
        
        # Вызов функции генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{additional_attribute_name_new[j]}%' or json_name like '%{additional_attribute_jsonName_new[j]}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                additional_attribute_name_new[j]
            ],
            'jsonNames': [
                additional_attribute_jsonName_new[j]
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for i in range(count_json):
                for key in param_ALL_additional_attribute_search.get('content'):
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor,
                                                          param_ALL_additional_attribute_search.get('content').get(key),
                                                          "additional_attribute",
                                                          f" name like '%{additional_attribute_name_new[j]}%' or json_name like '%{additional_attribute_jsonName_new[j]}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute_search.get('content').get(key)} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute_search.get('content').get(key)} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
        logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Частичное совпадение')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55284")
    def test_c55284_main(self, profile_api, cn, dbCursor):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55284")
        logging.info("Получение списка дополнительных атрибутов (POST). Частичное совпадение")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Функция генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        name_new_part = additional_attribute_jsonName_new[j][:7]
        json_name_new_part = additional_attribute_jsonName_new[j][:7]
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Получаем количество записей в БД
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{name_new_part}%' or json_name like '%{json_name_new_part}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                name_new_part
            ],
            'jsonNames': [
                json_name_new_part
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 200, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 200, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        count_json = len(jmespath.search(f"content[*]", response_json))
        
        assert count_record_db_cond == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            
            i = 0
            while i < count_json:
                json_id = jmespath.search(f"content[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                          "additional_attribute",
                                                          f"id = {json_id}")
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ############################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующий names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55276")
    def test_c55276_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55276")
        logging.info("Получение списка дополнительных атрибутов (POST). Несуществующий names")
        
        # Номер итерации для генерации данных
        j = 5  # Для списка additional_attribute_<param>_new
        
        # Вызов функции генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonName_new[j]}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                additional_attribute_name_wrong
            ],
            'jsonNames': [
                additional_attribute_jsonName_new[j]
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                for key in param_ALL_additional_attribute_search.get('content'):
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor,
                                                          param_ALL_additional_attribute_search.get('content').get(key),
                                                          "additional_attribute",
                                                          f"name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonName_new[j]}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute_search.get('content').get(key)} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute_search.get('content').get(key)} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
    
    ############################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующий jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55274")
    def test_c55274_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55274")
        logging.info("Получение списка дополнительных атрибутов (POST). Несуществующий jsonNames")
        
        # Номер итерации для генерации данных
        j = 5  # Для списка additional_attribute_<param>_new
        
        # Вызов функции генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{additional_attribute_name_new[j]}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                additional_attribute_name_new[j]
            ],
            'jsonNames': [
                additional_attribute_jsonNames_wrong
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                for key in param_ALL_additional_attribute_search.get('content'):
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor,
                                                          param_ALL_additional_attribute_search.get('content').get(key),
                                                          "additional_attribute",
                                                          f" name like '%{additional_attribute_name_new[j]}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute_search.get('content').get(key)} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute_search.get('content').get(key)} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ############################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующие names и jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55279")
    def test_c55279_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55279")
        logging.info("Получение списка дополнительных атрибутов (POST). Несуществующие names и jsonNames")
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                additional_attribute_name_wrong
            ],
            'jsonNames': [
                additional_attribute_jsonNames_wrong
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                for key in param_ALL_additional_attribute_search.get('content'):
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor,
                                                          param_ALL_additional_attribute_search.get('content').get(key),
                                                          "additional_attribute",
                                                          f" name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute_search.get('content').get(key)} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute_search.get('content').get(key)} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ############################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55270")
    def test_c55270_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55270")
        logging.info("Получение списка дополнительных атрибутов (POST). Указан только names")
        
        # Номер итерации для генерации данных
        j = 5  # Для списка additional_attribute_<param>_new
        
        # Вызов функции генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{additional_attribute_name_new[j]}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                additional_attribute_name_new[j]
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                for key in param_ALL_additional_attribute_search.get('content'):
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor,
                                                          param_ALL_additional_attribute_search.get('content').get(key),
                                                          "additional_attribute",
                                                          f" name like '%{additional_attribute_name_new[j]}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute_search.get('content').get(key)} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute_search.get('content').get(key)} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ############################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55271")
    def test_c55271_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55271")
        logging.info("Получение списка дополнительных атрибутов (POST). Указан только jsonNames")
        
        # Номер итерации для генерации данных
        j = 5  # Для списка additional_attribute_<param>_new
        
        # Вызов функции генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonName_new[j]}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'jsonNames': [
                additional_attribute_jsonName_new[j]
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                for key in param_ALL_additional_attribute_search.get('content'):
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor,
                                                          param_ALL_additional_attribute_search.get('content').get(key),
                                                          "additional_attribute",
                                                          f"json_name like '%{additional_attribute_jsonName_new[j]}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute_search.get('content').get(key)} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute_search.get('content').get(key)} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ############################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Не указаны names и jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55272")
    def test_c55272_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55272")
        logging.info("Получение списка дополнительных атрибутов (POST). Не указаны names и jsonNames")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record = count_record_db(dbCursor, 'additional_attribute')
        
        size_pages = 20
        page = 0  # Задаем номер страницы
        sort = 'id:ASC'  # Задаем сортировку
        
        body = {}
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers,
                                    params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Т.к отображаем 20 записей
        assert count_json == 20, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort,
                               count_record)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                json_id = jmespath.search(f"content[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                for key in param_ALL_additional_attribute_search.get('content'):
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor,
                                                          param_ALL_additional_attribute_search.get('content').get(key),
                                                          "additional_attribute",
                                                          f"id = {json_id}")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute_search.get('content').get(key)} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute_search.get('content').get(key)} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Сортировка DESC')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55280")
    def test_c55280_main(self, profile_api, cn, dbCursor):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55280")
        logging.info("Получение списка дополнительных атрибутов (POST). Сортировка DESC")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Функция генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        name_new_part = additional_attribute_jsonName_new[j][:7]
        json_name_new_part = additional_attribute_jsonName_new[j][:7]
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Получаем количество записей в БД
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{name_new_part}%' or json_name like '%{json_name_new_part}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:DESC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                name_new_part
            ],
            'jsonNames': [
                json_name_new_part
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 200, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 200, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        count_json = len(jmespath.search(f"content[*]", response_json))
        
        assert count_record_db_cond == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка сортировки"):
            # Вызов функции проверки сортировки списка
            sort_list(sort, count_json, response_json)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                json_id = jmespath.search(f"content[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                # id_list.append(json_id)  # Записываем json_id в список для проверки сортировки
                # assert id_list == sorted(id_list, reverse = True), 'Список не отсортирован'
                
                logging.debug(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                          "additional_attribute",
                                                          f"id = {json_id}")
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей до {count_record_before}, после: {count_record_after}")
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Сортировка ASC')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58095")
    def test_c58095_main(self, profile_api, cn, dbCursor):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58095")
        logging.info("Получение списка дополнительных атрибутов (POST). Сортировка ASC")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Функция генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        name_new_part = additional_attribute_jsonName_new[j][:7]
        json_name_new_part = additional_attribute_jsonName_new[j][:7]
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Получаем количество записей в БД
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{name_new_part}%' or json_name like '%{json_name_new_part}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'id:asc'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                name_new_part
            ],
            'jsonNames': [
                json_name_new_part
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 200, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 200, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        count_json = len(jmespath.search(f"content[*]", response_json))
        
        assert count_record_db_cond == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка сортировки"):
            # Вызов функции проверки сортировки списка
            sort_list(sort, count_json, response_json)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                json_id = jmespath.search(f"content[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                # id_list.append(json_id)  # Записываем json_id в список для проверки сортировки
                # assert id_list == sorted(id_list, reverse = True), 'Список не отсортирован'
                
                logging.debug(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                          "additional_attribute",
                                                          f"id = {json_id}")
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Сортировка json_name ASC')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58097")
    @pytest.mark.xfail  # Падает, но оно и не должно сортироваться по этому параметру
    def test_c58097_asc(self, profile_api, cn, dbCursor):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58097")
        logging.info("Получение списка дополнительных атрибутов (POST). Сортировка json_name ASC")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Функция генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        name_new_part = additional_attribute_jsonName_new[j][:7]
        json_name_new_part = additional_attribute_jsonName_new[j][:7]
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Получаем количество записей в БД
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{name_new_part}%' or json_name like '%{json_name_new_part}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'json_name:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                name_new_part
            ],
            'jsonNames': [
                json_name_new_part
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 200, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 200, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        count_json = len(jmespath.search(f"content[*]", response_json))
        
        assert count_record_db_cond == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка сортировки"):
            # Вызов функции проверки сортировки списка
            sort_list(sort, count_json, response_json)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                json_id = jmespath.search(f"content[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                
                logging.debug(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                          "additional_attribute",
                                                          f"id = {json_id}")
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Сортировка json_name DESC')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/58097")
    @pytest.mark.xfail  # Падает, но оно и не должно сортироваться по этому параметру
    def test_c58097_desc(self, profile_api, cn, dbCursor):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/58097")
        logging.info("Получение списка дополнительных атрибутов (POST). Сортировка json_name DESC")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Функция генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        name_new_part = additional_attribute_jsonName_new[j][:7]
        json_name_new_part = additional_attribute_jsonName_new[j][:7]
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Получаем количество записей в БД
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{name_new_part}%' or json_name like '%{json_name_new_part}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        sort = 'json_name:desc'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                name_new_part
            ],
            'jsonNames': [
                json_name_new_part
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 200, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 200, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        count_json = len(jmespath.search(f"content[*]", response_json))
        
        assert count_record_db_cond == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка сортировки"):
            # Вызов функции проверки сортировки списка
            sort_list(sort, count_json, response_json)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_json:
                json_id = jmespath.search(f"content[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                
                logging.debug(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                          "additional_attribute",
                                                          f"id = {json_id}")
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort)
        
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Разные номера страниц')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55281")
    @pytest.mark.parametrize("page", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_c55281_main(self, profile_api, cn, dbCursor, page):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55281")
        logging.info("Получение списка дополнительных атрибутов (POST). Разные номера страниц")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record = count_record_db(dbCursor, 'additional_attribute')
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        # size_pages = record_size_pages(count_record_db_cond)
        size_pages = count_record // 25 + 1
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {}
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 200, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 200, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        count_json = len(jmespath.search(f"content[*]", response_json))
        
        assert size_pages == count_json, 'Количество записей на странице и json объектов не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            
            i = 0
            while i < count_json:
                json_id = jmespath.search(f"content[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                logging.debug(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                          "additional_attribute",
                                                          f"id = {json_id}")
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort,
                               count_record)
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Разное количество записей на одной странице')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55281")
    @pytest.mark.parametrize("size_pages", [1, 5, 10, 15, 20, 25, 50, 70, 75])
    def test_c55282_main(self, profile_api, cn, dbCursor, size_pages):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55281")
        logging.info("Получение списка дополнительных атрибутов (POST). Разное количество записей на одной странице")
        
        #  Параметр для поиска
        param_find = 'AD'
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        # size_pages = record_size_pages(count_record_db_cond)
        # size_pages = count_record // 25 + 1
        sort = 'id:ASC'  # Задаем сортировку
        page = 0
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            "names": [
                param_find
            ],
            "jsonNames": [
                param_find
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 200, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 200, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД до выполнения запроса
        count_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"name like '%{param_find}%' or name like '%{param_find.lower()}%' or json_name like '%{param_find}%' or json_name like '%{param_find.lower()}%'")
        
        count_json = len(jmespath.search(f"content[*]", response_json))
        
        assert size_pages == count_json, 'Количество записей на странице и json объектов не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            
            i = 0
            while i < count_json:
                json_id = jmespath.search(f"content[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                logging.debug(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"content[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                          "additional_attribute",
                                                          f"id = {json_id}")
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_additional_attribute_search, response_json, sort,
                               count_record)
        
        logging.info(f"Тест завершен успешно.")
