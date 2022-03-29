import allure
import jmespath

from conftest import *
from functions import gen_test_add_attribute_id, parse_response_json, assert_status_code, check_response_schema, \
    count_record_db_condition, reformatted_param, params_record_db_condition, count_record_db
from json_schemas import GET_profile_attributes_additional_200_main_schema


# Todo узнать почему тут таймзона такая же в json как в БД, а у баз. атрибутов нет

@allure.epic("Получение списка дополнительных атрибутов (GET)")
@allure.description('Получение списка дополнительных атрибутов (GET)')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test200:
    
    @allure.epic("Получение списка дополнительных атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий (полное совпадение')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55255")
    @pytest.mark.smoke
    def test_c55255_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55255")
        logging.info("Получение списка дополнительных атрибутов (GET). Прямой сценарий (полное совпадение)")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Вызов функции создание доп. атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Параметры для GET метода
        params = {
            "names": f"{additional_attribute_name_new[j]}",
            "jsonNames": f"{additional_attribute_jsonName_new[j]}"
        }
        
        response = profile_api.get("/profile/attributes/additional/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Вызываем GET метод
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
            
            # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name like '%{additional_attribute_name_new[j]}%' and json_name like '%{additional_attribute_jsonName_new[j]}%'")
        
        assert count_json == count_record_db_cond, "Кол-во записей в БД и json не совпадает"
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_record_db_cond:
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[
                        key], "additional_attribute",
                                                          f" name like '%{additional_attribute_name_new[j]}%' and json_name like '%{additional_attribute_jsonName_new[j]}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Частичное совпадение')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55267")
    # Старый - https://git.dev-mcx.ru/zenit/profile-service/-/issues/42
    def test_c55267_main(self, profile_api, cn, dbCursor):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55267")
        logging.info("Получение списка дополнительных атрибутов (GET). Частичное совпадение")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Функция генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        name_new_part = additional_attribute_jsonName_new[j][:7]
        json_name_new_part = additional_attribute_jsonName_new[j][:7]
        
        # Указываем данные полученные на 1 шаге из переменных
        params = {"names": f"{name_new_part}",
                  "jsonNames": f"{json_name_new_part}"}
        
        response = profile_api.get("/profile/attributes/additional/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 200, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 200, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
            # Получаем количество записей в БД
        count_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"name like '%{name_new_part}%' or json_name like '%{json_name_new_part}%'")
        
        count_json = len(jmespath.search(f"[*]", response_json))
        
        assert count_record == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_record:
                json_id = jmespath.search(f"[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                logging.debug(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
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
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Некорректный names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55262")
    def test_c55262_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55262")
        logging.info("Получение списка дополнительных атрибутов (GET). Некорректный names")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Вызываем функцию генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Указываем данные запроса
        params = {
            "names": f"{additional_attribute_name_wrong}",
            "jsonNames": f"{additional_attribute_jsonName_new[j]}"
        }
        
        response = profile_api.get("/profile/attributes/additional/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
            # Получаем количество записей в БД
        count_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonName_new[j]}%'")
        
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        assert count_record == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_record:
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[
                        key], "additional_attribute",
                                                          f"name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonName_new[j]}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Некорректный jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55263")
    def test_c55263_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55263")
        logging.info("Получение списка дополнительных атрибутов (GET). Некорректный jsonNames")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Вызываем функцию генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Указываем данные запроса
        params = {
            "names": f"{additional_attribute_name_new[j]}",
            "jsonNames": f"{additional_attribute_jsonNames_wrong}"
        }
        response = profile_api.get("/profile/attributes/additional/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
            
            # Получаем количество записей в БД
        count_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"name like '%{additional_attribute_name_new[j]}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
        
        count_json = len(jmespath.search(f"[*]", response_json))
        
        assert count_record == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_record:
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[
                        key], "additional_attribute",
                                                          f" name like '%{additional_attribute_name_new[j]}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55256")
    def test_c55256_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55256")
        logging.info("Получение списка дополнительных атрибутов (GET). Указан только names")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Вызываем функцию генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Указываем данные запроса
        params = {
            "names": f"{additional_attribute_name_new[j]}"
        }
        response = profile_api.get("/profile/attributes/additional/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
            
            # Получаем количество записей в БД
        count_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"name like '%{additional_attribute_name_new[j]}%'")
        
        count_json = len(jmespath.search(f"[*]", response_json))
        
        assert count_record == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_record:
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[
                        key], "additional_attribute",
                                                          f" name like '%{additional_attribute_name_new[j]}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55257")
    def test_c55257_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55257")
        logging.info("Получение списка дополнительных атрибутов (GET). Указан только jsonNames")
        
        # Номер итерации для генерации данных
        j = 5
        
        # Вызываем функцию генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, j)
        
        # Указываем данные из переменных
        params = {
            "jsonNames": f"{additional_attribute_jsonName_new[j]}"
        }
        response = profile_api.get("/profile/attributes/additional/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД
        count_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"json_name like '%{additional_attribute_jsonName_new[j]}%'")
        
        count_json = len(jmespath.search(f"[*]", response_json))
        
        assert count_record == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_record:
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[
                        key], "additional_attribute",
                                                          f"json_name like '%{additional_attribute_jsonName_new[j]}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Не указаны jsonNames и names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55258")
    def test_c55258_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55258")
        logging.info("Получение списка дополнительных атрибутов (GET). Не указаны jsonNames и names")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record = count_record_db(dbCursor, 'additional_attribute')
        
        # Отправляем запрос
        response = profile_api.get(
                "/profile/attributes/additional/")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество подписей до выполнения запроса: {count_record}, после: {count_json}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_record:
                json_id = jmespath.search(f"[{i}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                logging.debug(f'Проверяем атрибут - {json_id} объект - {i}')
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
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
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка дополнительных атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Некорректные данные полей names и jsonNames')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55264")
    def test_c55264_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55264")
        logging.info("Получение списка дополнительных атрибутов (GET). Некорректные данные полей names и jsonNames")
        
        # Указываем данные запроса
        params = {
            "names": f"{additional_attribute_name_wrong}",
            "jsonNames": f"{additional_attribute_jsonNames_wrong}"
        }
        response = profile_api.get("/profile/attributes/additional/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_additional_200_main_schema)  # Проверка JSON-схемы ответа
            
            # Получаем количество записей в БД
        count_record = count_record_db_condition(dbCursor, 'additional_attribute',
                                                 f"name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
        
        count_json = len(jmespath.search(f"[*]", response_json))
        
        assert count_record == count_json, 'Количество записей в БД и json ответе не совпадает'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0
            while i < count_record:
                for key in param_ALL_additional_attribute:
                    json_value = jmespath.search(f"[{i}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Функция реформатирования параметров
                    json_value = reformatted_param(key, json_value)
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[
                        key], "additional_attribute",
                                                          f" name like '%{additional_attribute_name_wrong}%' or json_name like '%{additional_attribute_jsonNames_wrong}%'")
                    
                    # Логирование, для отладки
                    logging.debug(f"№ строки - {i} - JSON-данные ключ - {key} - {json_value} ")
                    logging.debug(
                            f"№ строки - {i} - БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                i += 1
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
