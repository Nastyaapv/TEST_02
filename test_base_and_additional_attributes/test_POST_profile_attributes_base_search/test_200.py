import allure
import jmespath

from conftest import *
from functions import parse_request_json, check_response_schema, gen_test_base_attribute_id, parse_response_json, \
    assert_status_code, \
    reformatted_param, params_record_db_condition, count_record_db_condition, count_record_db, record_size_pages, \
    sort_list, check_param_schema

from json_schemas import GET_profile_attributes_base_search_200_main_schema


@allure.epic("Получение списка базовых атрибутов (POST)")
@allure.description('Получение списка базовых атрибутов (POST)')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test200:
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий (полное совпадение)')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54643")
    @pytest.mark.smoke
    def test_c54643_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54643")
        logging.info("Получение списка базовых атрибутов (POST). Прямой сценарий (полное совпадение) ")
        
        # Тут полное совпадение значит запись только одна будет
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_<param>_new
        
        # Вызываем функцию генерации base attribute ID
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'base_attribute')
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{base_attribute_name_new[i]}%' or identity like '%{base_attribute_identity_new[i]}%'")
        
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
                base_attribute_name_new[i]
            ],
            'identities': [
                base_attribute_identity_new[i]
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[0].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"json_name = '{base_attribute_json_name_new[i]}'")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort)
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'base_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Частичное совпадение')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54649")
    def test_c54649_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54643")
        logging.info("Получение списка базовых атрибутов (POST). Частичное совпадение")
        
        # Тут полное совпадение значит запись только одна будет
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_<param>_new
        
        # Вызываем функцию генерации base attribute ID
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        name_new_part = base_attribute_name_new[i][:7]
        identity_new_part = base_attribute_identity_new[i][:7]
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'base_attribute')
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{name_new_part}%' or name like '%{name_new_part.lower()}%' or "
                                                         f"identity like '%{identity_new_part}%' or identity like '%{identity_new_part.lower()}%'")
        
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
            'identities': [
                identity_new_part
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"id = {json_id}")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort)
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'base_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующий names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54647")
    def test_c54647_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54647")
        logging.info("Получение списка базовых атрибутов (POST). Несуществующий names")
        
        # Тут полное совпадение значит запись только одна будет
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_<param>_new
        
        # Вызываем функцию генерации base attribute ID
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{base_attribute_name_wrong}%' or identity like '%{base_attribute_identity_new[i]}%'")
        
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
                base_attribute_name_wrong
            ],
            'identities': [
                base_attribute_identity_new[i]
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"id = {json_id}")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort)
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующий identities')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54648")
    def test_c54648_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54648")
        logging.info("Получение списка базовых атрибутов (POST). Несуществующий identities")
        
        # Тут полное совпадение значит запись только одна будет
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_<param>_new
        
        # Вызываем функцию генерации base attribute ID
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{base_attribute_name_new[i]}%' or identity like '%{base_attribute_identity_wrong}%'")
        
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
                base_attribute_name_new[i]
            ],
            'identities': [
                base_attribute_identity_wrong
            
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"id = {json_id}")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort)
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующие names и identities')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54653")
    def test_c54653_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54653")
        logging.info("Получение списка базовых атрибутов (POST). Несуществующие names и identities")
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{base_attribute_name_wrong}%' or identity like '%{base_attribute_identity_wrong}%'")
        
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
                base_attribute_name_wrong
            ],
            'identities': [
                base_attribute_identity_wrong
            
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"id = {json_id}")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort)
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54644")
    def test_c54644_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54644")
        logging.info("Получение списка базовых атрибутов (POST). Указан только names")
        
        # Тут полное совпадение значит запись только одна будет
        # Номер итерации для генерации данных base_attribute_<param>_new
        j = 2  # Для списка base_attribute_<param>_new
        
        # Вызываем функцию генерации base attribute ID
        gen_test_base_attribute_id(profile_api, dbCursor, j)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{base_attribute_name_new[j]}%'")
        
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
                base_attribute_name_new[j]
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"name like '%{base_attribute_name_new[j]}%'")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort)
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только identities')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54645")
    def test_c54645_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54645")
        logging.info("Получение списка базовых атрибутов (POST). Указан только identities")
        
        # Тут полное совпадение значит запись только одна будет
        # Номер итерации для генерации данных base_attribute_<param>_new
        j = 2  # Для списка base_attribute_<param>_new
        
        # Вызываем функцию генерации base attribute ID
        gen_test_base_attribute_id(profile_api, dbCursor, j)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"identity like '%{base_attribute_identity_new[j]}%'")
        
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
            'identities': [
                base_attribute_identity_new[j]
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"identity like '%{base_attribute_identity_new[j]}%'")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort)
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Разные виды сортировки')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55245")
    @pytest.mark.parametrize("sort", ['id:ASC', 'id:asc', 'id:desc', 'id:DESC', 'name:asc', 'name:desc'])
    def test_c55245_main(self, profile_api, cn, dbCursor, sort):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55245")
        logging.info("Получение списка базовых атрибутов (POST). Разные виды сортировки")
        
        #  Параметр для поиска
        param_find = 'BASE'
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{param_find}%' or name like '%{param_find.lower()}%' or identity like '%{param_find}%' or identity like '%{param_find.lower()}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        size_pages = record_size_pages(count_record_db_cond)
        page = 0  # Задаем номер страницы
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                param_find
            ],
            'identities': [
                param_find
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка сортировки"):
            # Вызов функции проверки сортировки списка
            sort_list(sort, count_json, response_json)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"id = {json_id}")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort)
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Разные номера страниц')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55247")
    @pytest.mark.parametrize("page", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_c55247_main(self, profile_api, cn, dbCursor, page):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55247")
        logging.info("Получение списка базовых атрибутов (POST). Разные номера страниц")
        
        #  Параметр для поиска
        param_find = 'BASE'
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{param_find}%' or name like '%{param_find.lower()}%' or "
                                                         f"identity like '%{param_find}%' or identity like '%{param_find.lower()}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        # size_pages = record_size_pages(count_record_db_cond)
        size_pages = count_record_db_cond // 25 + 1
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                param_find
            ],
            'identities': [
                param_find
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert size_pages == count_json, "Количество записей на странице и json объектов не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"id = {json_id}")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort,
                               count_record_db_cond)
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (POST)")
    @allure.feature('Проверка кода 200')
    @allure.story('Разное количество записей на одной странице')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55248")
    @pytest.mark.parametrize("size_pages", [1, 5, 10, 15, 20, 25, 50, 70])
    def test_c55248_main(self, profile_api, cn, dbCursor, size_pages):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55248")
        logging.info("Получение списка базовых атрибутов (POST). Разное количество записей на одной странице")
        
        #  Параметр для поиска
        param_find = 'BASE'
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{param_find}%' or name like '%{param_find.lower()}%' or "
                                                         f"identity like '%{param_find}%' or identity like '%{param_find.lower()}%'")
        
        # Вызов функции подсчета значения size на странице, исходя из кол-ва записей в БД
        # size_pages = record_size_pages(count_record_db_cond)
        # size_pages = count_record_db_cond // 25 + 1
        page = 0
        sort = 'id:ASC'  # Задаем сортировку
        
        params = {
            'page': page,
            'size': size_pages,
            'sort': sort
        }
        
        body = {
            'names': [
                param_find
            ],
            'identities': [
                param_find
            ]
            
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/base/search", headers = headers, params = params,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_search_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"content[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert size_pages == count_json, "Количество записей на странице и json объектов не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
        while i < count_json:
            json_id = jmespath.search(f"content[{i}].id",
                                      response_json)  # Ищем каждый параметр из файла с параметрами json
            logging.info(f'Проверяем атрибут - {json_id} объект - {i}')
            
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute_search.get('content'):
                json_value = jmespath.search(f"content[{i}].{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute_search.get('content').get(key),
                                                      'base_attribute',
                                                      f"id = {json_id}")
                
                # Логирование, для отладки
                logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                logging.debug(
                        f"№ строки - {i} - БД-данные - ключ БД {param_ALL_base_attribute_search.get('content').get(key)} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            i += 1
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Проверка page объектов схемы:"):
            check_param_schema(page, size_pages, param_ALL_base_attribute_search, response_json, sort,
                               count_record_db_cond)
        
        logging.info(f"Тест завершен успешно.")
