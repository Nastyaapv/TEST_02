import allure

from conftest import *
from functions import parse_response_json, check_response_schema, parse_request_json, count_record_db, \
    count_record_db_condition, assert_status_code
from json_schemas import schema_400_error


@allure.epic("Добавление дополнительных атрибутов получателей МГП")
@allure.description('Добавление дополнительных атрибутов получателей МГП')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test400:
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указано тело запроса')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52178")
    def test_c52178_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52178")
        logging.info('Добавление дополнительных атрибутов получателей МГП. Не указано тело запроса')
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor,
                                              'additional_attribute')
        
        body = {}
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]
        
        # Отправляем запрос
        response = profile_api.post("/profile/attributes/additional", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_400_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')
        
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    #############################################################################################
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 400')
    @allure.story('В теле не указан Name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52676")
    def test_c52676_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52676")
        logging.info('Добавление дополнительных атрибутов получателей МГП. В теле не указан Name')
        
        # Номер итерации для генерации данных additional_attribute_<param>_new
        i = 3
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        body = {
            "display": additional_attribute_display_new[i],
            "required": additional_attribute_required_new[i],
            # "name": f"{additional_attribute_name_new[i]}",
            "jsonName": f"{additional_attribute_jsonName_new[i]}",
            "fieldOrder": additional_attribute_fieldOrder_new[i],
            "fieldType": additional_attribute_fieldType_new[i],
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
        
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_400_error)  # Проверка JSON-схемы ответа
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 400, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 400, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"json_name = '{additional_attribute_jsonName_new[i]}'")
        
        # Проверяем наличие в БД по name и json_name
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД больше одной или вообще нет записей "
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor, 'additional_attribute')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    #############################################################################################
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные дополнительного атрибута')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52179")
    def test_c52179_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52179")
        logging.info(
                'Добавление дополнительных атрибутов получателей МГП. Некорректные данные дополнительного атрибута')
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        body = {
            "display": additional_attribute_display_new_wrong,
            "required": additional_attribute_required_new_wrong,
            "name": f"{additional_attribute_name_new_wrong}",
            "jsonName": f"{additional_attribute_jsonName_new_wrong}",
            "fieldOrder": additional_attribute_fieldOrder_new_wrong,
            "fieldType": additional_attribute_fieldType_new_wrong,
            "userType": f"{additional_attribute_userType_new_wrong}",
            "creationDate": f"{additional_attribute_creationDate_new_wrong}",
            "region": f"{additional_attribute_region_new_wrong}",
            "metadata": additional_attribute_metadata_new_wrong
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
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name = '{additional_attribute_name_new_wrong}' and json_name = '{additional_attribute_jsonName_new_wrong}'")
        
        # Проверяем наличие в БД по name и json_name
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД больше одной или вообще нет записей "
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor, 'additional_attribute')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    #############################################################################################
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные поля region')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54660")
    def test_c54660_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54660")
        logging.info(
                'Добавление дополнительных атрибутов получателей МГП. Некорректные данные поля region')
        
        # Номер итерации для генерации данных
        i = 6
        
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
            "region": f"{additional_attribute_region_new_wrong}",
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
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name = '{additional_attribute_name_new_wrong}' and json_name = '{additional_attribute_jsonName_new_wrong}'")
        
        # Проверяем наличие в БД по name и json_name
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД больше одной или вообще нет записей "
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor, 'additional_attribute')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    #############################################################################################
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные поля userType')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54662")
    def test_c54662_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54662")
        logging.info(
                'Добавление дополнительных атрибутов получателей МГП. Некорректные данные поля userType')
        
        # Номер итерации для генерации данных
        i = 6
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        body = {
            "display": additional_attribute_display_new[i],
            "required": additional_attribute_required_new[i],
            "name": f"{additional_attribute_name_new[i]}",
            "jsonName": f"{additional_attribute_jsonName_new[i]}",
            "fieldOrder": additional_attribute_fieldOrder_new[i],
            "fieldType": f"{additional_attribute_fieldType_new[i]}",
            "userType": f"{additional_attribute_userType_new_wrong}",
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
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name = '{additional_attribute_name_new_wrong}' and json_name = '{additional_attribute_jsonName_new_wrong}'")
        
        # Проверяем наличие в БД по name и json_name
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД больше одной или вообще нет записей "
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor, 'additional_attribute')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    #############################################################################################
    
    @allure.epic("Добавление дополнительных атрибутов получателей МГП")
    @allure.feature('Проверка кода 400')
    @allure.story('Некорректные данные поля fieldType')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54663")
    @pytest.mark.xfail  # TODO завести дефект на код 500
    def test_c54663_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54663")
        logging.info(
                'Добавление дополнительных атрибутов получателей МГП. Некорректные данные поля fieldType')
        
        # Номер итерации для генерации данных
        i = 6
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        body = {
            "display": additional_attribute_display_new[i],
            "required": additional_attribute_required_new[i],
            "name": f"{additional_attribute_name_new[i]}",
            "jsonName": f"{additional_attribute_jsonName_new[i]}",
            "fieldOrder": additional_attribute_fieldOrder_new[i],
            "fieldType": f"{additional_attribute_fieldType_new_wrong}",
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
            assert_status_code(response, 400)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f"name = '{additional_attribute_name_new_wrong}' and json_name = '{additional_attribute_jsonName_new_wrong}'")
        
        # Проверяем наличие в БД по name и json_name
        with allure.step("Проверка того, что в БД есть запись"):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД больше одной или вообще нет записей "
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor, 'additional_attribute')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
    
    #############################################################################################
