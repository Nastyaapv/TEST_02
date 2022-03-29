import allure
import jmespath

from conftest import *
from functions import parse_response_json, assert_status_code, \
    reformatted_param, params_record_db_condition, count_record_db_condition, count_record_db, parse_request_json, \
    gen_test_add_attribute_id


@allure.epic("Добавление дополнительных атрибутов получателей МГП")
@allure.description('Добавление дополнительных атрибутов получателей МГП')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test201:
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 201')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52174")
    @pytest.mark.smoke
    def test_c52174_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52174")
        logging.info("Добавление дополнительных атрибутов получателей МГП. Прямой сценарий ")
        
        # Номер итерации для генерации данных additional_attribute_<param>_new
        i = 0
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        body = {
            "display": additional_attribute_display_new[i],
            "required": additional_attribute_required_new[i],
            "name": f"{additional_attribute_name_new[i]}",
            "jsonName": f"{additional_attribute_jsonName_new[i]}",
            "fieldOrder": additional_attribute_fieldOrder_new[i],
            "fieldType": f"{additional_attribute_fieldType_new[i]}",
            "userType": f"{additional_attribute_userType_new[i]}",
            "creationDate": f"{additional_attribute_creationDate_new[i]}",
            "region": f"{additional_attribute_region_new[i]}",
            "metadata": additional_attribute_metadata_new[i]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name = '{additional_attribute_name_new[i]}' and json_name = '{additional_attribute_jsonName_new[i]}'")
        
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 1, f"В БД больше одной или вообще нет записей "
        
        # Получаем параметр в БД условию
        additional_attribute_id_new = params_record_db_condition(dbCursor, "id", "additional_attribute",
                                                                 f"name = '{additional_attribute_name_new[i]}' and json_name = '{additional_attribute_jsonName_new[i]}'")
        
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_new}")  # Записываем ответ метода GET в переменную response
        
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step(
                "Посмотрим совпадают ли отправленные данные, тому что сохранилось"):  # Записываем шаг в отчет allure
            for key in body:
                if key == 'creationDate':
                    continue
                request_json_value = jmespath.search(key, body)  # body_json
                response_json_value = jmespath.search(key, response_json)
                
                # Логирование, для отладки
                logging.debug(f"Отправленные JSON-данные ключ - {key} - {request_json_value} ")
                logging.debug(
                        f"Сохраненные JSON-данные ключ - {param_ALL_additional_attribute[key]} - {response_json_value}")
                
                assert request_json_value == response_json_value, 'Данные не совпадают'
            logging.info(f"Сохраненные данные соответствуют отправляемым")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for key in param_ALL_additional_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value)
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                      'additional_attribute',
                                                      f"id = {additional_attribute_id_new}")
                # Логирование, для отладки
                logging.debug(f"JSON-данные ключ - {key} - {json_value} ")
                logging.debug(f"БД-данные ключ - {param_ALL_additional_attribute[key]} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_record_before + 1 == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса изменилось")
        logging.info(f"Тест завершен успешно.")
    
    ##################################################################################
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 201')
    @allure.story('Такой дополнительный атрибут уже существует по name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52176")
    # Это не дефект - см. https://git.dev-mcx.ru/zenit/profile-service/-/issues/101
    def test_c52176_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52176")
        logging.info(
                "Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по name ")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызов функции генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, i)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor,
                                              'additional_attribute')  # Получаем количество записей в БД до выполнения запроса
        
        # Только name должен повторяться
        body = {
            "display": additional_attribute_display_new[i + 1],
            "required": additional_attribute_required_new[i + 1],
            "name": f"{additional_attribute_name_new[i]}",
            "jsonName": f"{additional_attribute_jsonName_new[i + 1]}",
            "fieldOrder": additional_attribute_fieldOrder_new[i + 1],
            "fieldType": f"{additional_attribute_fieldType_new[i + 1]}",
            "userType": f"{additional_attribute_userType_new[i + 1]}",
            "creationDate": f"{additional_attribute_creationDate_new[i + 1]}",
            "region": f"{additional_attribute_region_new[i + 1]}",
            "metadata": additional_attribute_metadata_new[i + 1]
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name = '{additional_attribute_name_new[i]}' and json_name = '{additional_attribute_jsonName_new[i + 1]}'")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД есть добавляемая запись "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 1, f"В БД больше одной или вообще нет записей "
            logging.info(f"В БД добавилась запись.")
        
        # Проверяем наличие записи в БД условию
        additional_attribute_id_new = params_record_db_condition(dbCursor, "id", "additional_attribute",
                                                                 f"name = '{additional_attribute_name_new[i]}' and json_name = '{additional_attribute_jsonName_new[i + 1]}'")
        
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_new}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step(
                "Посмотрим совпадают ли отправленные данные, тому что сохранилось"):  # Записываем шаг в отчет allure
            for key in body:
                if key == 'creationDate':
                    continue
                request_json_value = jmespath.search(key, body)  # body_json
                response_json_value = jmespath.search(key, response_json)
                
                # Логирование, для отладки
                logging.debug(f"Отправленные JSON-данные ключ - {key} - {request_json_value} ")
                logging.debug(
                        f"Сохраненные JSON-данные ключ - {param_ALL_additional_attribute[key]} - {response_json_value}")
                
                assert request_json_value == response_json_value, 'Данные не совпадают'
            logging.info(f"Сохраненные данные соответствуют отправляемым")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for key in param_ALL_additional_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value)
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                      'additional_attribute',
                                                      f"id = {additional_attribute_id_new}")
                # Логирование, для отладки
                logging.debug(f"JSON-данные ключ - {key} - {json_value} ")
                logging.debug(f"БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_record_before + 1 == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса изменилось")
        logging.info(f"Тест завершен успешно.")
    
    #############################################################################################
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 201')
    @allure.story('В теле не указан jsonName')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52675")
    # Это не дефект - см. https://git.dev-mcx.ru/zenit/profile-service/-/issues/103
    def test_c52675_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52675")
        logging.info('Добавление дополнительных атрибутов получателей МГП. В теле не указан jsonName')
        
        # Номер итерации для генерации данных
        i = 3
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        body = {
            "display": additional_attribute_display_new[i],
            "required": additional_attribute_required_new[i],
            "name": f"{additional_attribute_name_new[i]}",
            # "jsonName": f"{additional_attribute_jsonName_new[i]}",
            "fieldOrder": additional_attribute_fieldOrder_new[i],
            "fieldType": f"{additional_attribute_fieldType_new[i]}",
            "userType": f"{additional_attribute_userType_new[i]}",
            "creationDate": f"{additional_attribute_creationDate_new[i]}",
            "region": f"{additional_attribute_region_new[i]}",
            "metadata": additional_attribute_metadata_new[i]
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name = '{additional_attribute_name_new[i]}' and creation_date = (SELECT max(creation_date) FROM additional_attribute)")
        
        # Проверяем наличие в БД по name и json_name
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 1, f"В БД больше одной или вообще нет записей "
            logging.debug(f"В БД добавилась новая запись.")
        
        # Получаем значение параметра в БД по условию
        additional_attribute_id_new = params_record_db_condition(dbCursor, "id", "additional_attribute",
                                                                 f"name = '{additional_attribute_name_new[i]}' and creation_date = (SELECT max(creation_date) FROM additional_attribute)")
        
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_new}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step(
                "Посмотрим совпадают ли отправленные данные, тому что сохранилось"):  # Записываем шаг в отчет allure
            for key in body:
                if key == 'creationDate':
                    continue
                request_json_value = jmespath.search(key, body)  # body_json
                response_json_value = jmespath.search(key, response_json)
                
                # Логирование, для отладки
                logging.debug(f"Отправленные JSON-данные ключ - {key} - {request_json_value} ")
                logging.debug(
                        f"Сохраненные JSON-данные ключ - {param_ALL_additional_attribute[key]} - {response_json_value}")
                
                assert request_json_value == response_json_value, 'Данные не совпадают'
            logging.info(f"Сохраненные данные соответствуют отправляемым")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for key in param_ALL_additional_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value)
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_additional_attribute[key],
                                                      'additional_attribute',
                                                      f"id = {additional_attribute_id_new}")
                # Логирование, для отладки
                logging.debug(f"JSON-данные ключ - {key} - {json_value} ")
                logging.debug(f"БД-данные - ключ БД {param_ALL_additional_attribute[key]} - {db_query}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_additional_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            
            logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
            
            # Получаем количество записей в БД после выполнения запроса
            count_record_after = count_record_db(dbCursor, 'additional_attribute')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before + 1 == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса изменилось")
        logging.info(f"Тест завершен успешно.")
