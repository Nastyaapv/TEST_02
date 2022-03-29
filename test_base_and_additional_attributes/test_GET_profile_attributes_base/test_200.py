import allure
import jmespath

from conftest import *
from functions import check_response_schema, gen_test_base_attribute_id, parse_response_json, assert_status_code, \
    reformatted_param, params_record_db_condition, count_record_db_condition, count_record_db
from json_schemas import GET_profile_attributes_base_200_main_schema


# Todo узнать почему тут таймзона на 3 часа больше в json чем в БД, а у доп. атрибутов нет

@allure.epic("Получение списка базовых атрибутов (GET)")
@allure.description('Получение списка базовых атрибутов (GET)')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test200:
    
    @allure.epic("Получение списка базовых атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий (Полное совпадение)')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52149")
    @pytest.mark.smoke
    def test_c52149_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52149")
        logging.info("Получение списка базовых атрибутов (GET). Прямой сценарий(Полное совпадение)")
        
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_name_new
        
        # Генерим базовый атрибут
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Параметры для GET метода
        params = {
            "names": f"{base_attribute_name_new[i]}",
            "identities": f"{base_attribute_identity_new[i]}"
        }
        
        response = profile_api.get("/profile/attributes/base/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name like '%{base_attribute_name_new[i]}%' and identity like '%{base_attribute_identity_new[i]}%'")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            j = 0
            # Сверяем все строки из файла
            while j < count_record_db_cond:
                for key in param_ALL_base_attribute:
                    json_value = jmespath.search(f"[{j}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value, 'base_attribute')
                    
                    # Получаем значение записи в БД по условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[key],
                                                          'base_attribute',
                                                          f"name like '%{base_attribute_name_new[i]}%' and identity like '%{base_attribute_identity_new[i]}%'")
                    
                    logging.debug(f'№ объекта - {j}, параметр в БД {param_ALL_base_attribute[key]} - {db_query}')
                    logging.debug(f'№ объекта - {j}, параметр в json {key} - {json_value}')
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                
                j += 1
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
            logging.info(f"Тест завершен. Успешно")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Не указаны identities и names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52152")
    def test_c52152_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52152")
        logging.info("Получение списка базовых атрибутов. Не указаны identities и names")
        
        # Получаем количество записей в БД по условию
        count_record = count_record_db(dbCursor, 'base_attribute')
        
        # Отправляем запрос
        response = profile_api.get("/profile/attributes/base/")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            j = 0
            # Сверяем все строки из файла
            while j < count_record:
                json_id = jmespath.search(f"[{j}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                for key in param_ALL_base_attribute:
                    json_value = jmespath.search(f"[{j}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value, 'base_attribute')
                    
                    # Получаем значение записи в БД по условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[key],
                                                          'base_attribute',
                                                          f"id = {json_id}")
                    
                    logging.debug(f'№ объекта - {j}, параметр в БД {param_ALL_base_attribute[key]} - {db_query}')
                    logging.debug(f'№ объекта - {j}, параметр в json {key} - {json_value}')
                    
                    assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                j += 1
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество записей в json: {count_json}, в БД: {count_record}"
            logging.debug(f"Количество записей в БД = {count_json}")
        logging.info(f"Тест завершен успешно.")
    
    #########################################################################################
    @allure.epic("Получение списка базовых атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Частичное совпадение')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/53752")
    # Не дефект - https://git.dev-mcx.ru/zenit/profile-service/-/issues/43
    def test_c53752_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/53752")
        logging.info("Получение списка базовых атрибутов. Частичное совпадение")
        
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_name_new
        
        # Генерим базовый атрибут
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        base_attribute_part_name = base_attribute_name_new[i][:5]
        base_attribute_part_identity = base_attribute_identity_new[i][:5]
        
        params = {
            "names": f"{base_attribute_part_name}",
            "identities": f"{base_attribute_part_identity}"
        }
        
        response = profile_api.get("/profile/attributes/base/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond_part = count_record_db_condition(dbCursor, 'base_attribute',
                                                              f"name like '%{base_attribute_part_name}%' or identity like '%{base_attribute_part_identity}%'")
        logging.debug(f'Всего атрибутов - {count_record_db_cond_part}')
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            j = 0
            # Сверяем все строки из файла
            while j < count_record_db_cond_part:
                json_id = jmespath.search(f"[{j}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                logging.debug(f'Проверяем атрибут - {json_id} объект - {j}')
                for key in param_ALL_base_attribute:
                    json_value = jmespath.search(f"[{j}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value, 'base_attribute')
                    
                    # Получаем значение записи в БД по условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[key],
                                                          'base_attribute',
                                                          f"id = {json_id}")
                    
                    logging.debug(f'№ объекта - {j}, параметр в БД {param_ALL_base_attribute[key]} - {db_query}')
                    logging.debug(f'№ объекта - {j}, параметр в json {key} - {json_value}')
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                j += 1
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record_db_cond_part, f"Количество записей в json: {count_json}, в БД: {count_record_db_cond_part}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52150")
    def test_c52150_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52150")
        logging.info("Получение списка базовых атрибутов. Указан только names")
        
        i = 2  # Для списка base_attribute_name_new
        
        # Генерим базовый атрибут
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Указываем данные запроса
        params = {"names": f"{base_attribute_name_new[i]}"}
        response = profile_api.get("/profile/attributes/base/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'base_attribute',
                                                 f"name like '%{base_attribute_name_new[i]}%'")
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            j = 0
            # Сверяем все строки из файла
            while j < count_record:
                json_id = jmespath.search(f"[{j}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                for key in param_ALL_base_attribute:
                    json_value = jmespath.search(f"[{j}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value, 'base_attribute')
                    
                    # Получаем значение записи в БД по условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[key],
                                                          'base_attribute',
                                                          f"id = {json_id}")
                    
                    logging.debug(f'№ объекта - {j}, параметр в БД {param_ALL_base_attribute[key]} - {db_query}')
                    logging.debug(f'№ объекта - {j}, параметр в json {key} - {json_value}')
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                j += 1
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество записей в json: {count_json}, в БД: {count_record}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Указан только identities')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52151")
    def test_c52151_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52151")
        logging.info("Получение списка базовых атрибутов (GET). Указан только identities")
        
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_<param>_new
        
        # Генерим базовый атрибут
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Указываем данные запроса
        params = {"identities": f"{base_attribute_identity_new[i]}"}
        
        response = profile_api.get("/profile/attributes/base/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'base_attribute',
                                                 f"identity like '%{base_attribute_identity_new[i]}%'")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            j = 0
            # Сверяем все строки из файла
            while j < count_record:
                json_id = jmespath.search(f"[{j}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                for key in param_ALL_base_attribute:
                    json_value = jmespath.search(f"[{j}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value, 'base_attribute')
                    
                    # Получаем значение записи в БД по условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[key],
                                                          'base_attribute',
                                                          f"id = {json_id}")
                    
                    logging.debug(f'№ объекта - {j}, параметр в БД {param_ALL_base_attribute[key]} - {db_query}')
                    logging.debug(f'№ объекта - {j}, параметр в json {key} - {json_value}')
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                j += 1
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество записей в json: {count_json}, в БД: {count_record}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Некорректный names')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52153")
    #  Не дефект https://git.dev-mcx.ru/zenit/profile-service/-/issues/39
    def test_c52153_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52153")
        logging.info("Получение списка базовых атрибутов (GET). Некорректный names")
        
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_name_new
        
        # Генерим базовый атрибут
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Указываем данные запроса
        params = {
            "names": f"{base_attribute_name_wrong}",
            "identities": f"{base_attribute_identity_new[i]}"
        }
        response = profile_api.get("/profile/attributes/base",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'base_attribute',
                                                 f"name like '%{base_attribute_name_wrong}%' or identity like '%{base_attribute_identity_new[i]}%'")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            j = 0
            # Сверяем все строки из файла
            while j < count_record:
                json_id = jmespath.search(f"[{j}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                for key in param_ALL_base_attribute:
                    json_value = jmespath.search(f"[{j}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value, 'base_attribute')
                    
                    # Получаем значение записи в БД по условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[key],
                                                          'base_attribute',
                                                          f"id = {json_id}")
                    
                    logging.debug(f'№ объекта - {j}, параметр в БД {param_ALL_base_attribute[key]} - {db_query}')
                    logging.debug(f'№ объекта - {j}, параметр в json {key} - {json_value}')
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                j += 1
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество записей в json: {count_json}, в БД: {count_record}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    
    @allure.epic("Получение списка базовых атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Некорректный identities')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52678")
    # Не дефект - https://git.dev-mcx.ru/zenit/profile-service/-/issues/40
    def test_c52678_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52678")
        logging.info("Получение списка базовых атрибутов (GET). Некорректный identities")
        
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 2  # Для списка base_attribute_name_new
        
        # Генерим базовый атрибут
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Указываем данные запроса
        params = {
            "names": f"{base_attribute_name_new[i]}",
            "identities": f"{base_attribute_identity_wrong}"
        }
        response = profile_api.get("/profile/attributes/base/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'base_attribute',
                                                 f"name like '%{base_attribute_name_new[i]}%' or identity like '%{base_attribute_identity_wrong}%'")
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            j = 0
            # Сверяем все строки из файла
            while j < count_record:
                json_id = jmespath.search(f"[{j}].id",
                                          response_json)  # Ищем каждый параметр из файла с параметрами json
                for key in param_ALL_base_attribute:
                    json_value = jmespath.search(f"[{j}].{key}",
                                                 response_json)  # Ищем каждый параметр из файла с параметрами json
                    
                    # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                    json_value = reformatted_param(key, json_value, 'base_attribute')
                    
                    # Получаем значение записи в БД по условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[key],
                                                          'base_attribute',
                                                          f"id = {json_id}")
                    logging.debug(f'№ объекта - {j}, параметр в БД {param_ALL_base_attribute[key]} - {db_query}')
                    logging.debug(f'№ объекта - {j}, параметр в json {key} - {json_value}')
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
                j += 1
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество записей в json: {count_json}, в БД: {count_record}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################################################################################################################################
    @allure.epic("Получение списка базовых атрибутов (GET)")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующие names и identities')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54624")
    def test_c54624_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54624")
        logging.info("Получение списка базовых атрибутов (GET). Несуществующие names и identities")
        
        # Указываем данные запроса
        params = {
            "names": f"{base_attribute_name_wrong}",
            "identities": f"{base_attribute_identity_wrong}"
        }
        response = profile_api.get("/profile/attributes/base/",
                                   params = params)  # Записываем ответ метода GET в переменную response
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor, 'base_attribute',
                                                 f"name like '%{base_attribute_name_wrong}%' or identity like '%{base_attribute_identity_wrong}%'")
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_attributes_base_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == 0, f"Количество записей в json: {count_json}, а должно быть - 0"
            assert count_json == count_record, f"Количество записей в json: {count_json}, в БД: {count_record}"
            logging.debug(f"Количество записей в БД = {count_json}")
        
        logging.info(f"Тест завершен успешно.")
