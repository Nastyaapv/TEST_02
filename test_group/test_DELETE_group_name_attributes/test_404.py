import allure

from conftest import *
from functions import check_response_schema, gen_del_group, assert_status_code, count_record_db_condition, \
    count_record_db, parse_response_json, parse_request_json, gen_test_add_attribute_id
from json_schemas import schema_404_error


@allure.epic("Удалить список атрибутов из группы")
@allure.description('Удалить список атрибутов из группы')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test404:
    
    @allure.epic("Удалить список атрибутов из группы")
    @allure.feature('Проверка кода 404')
    @allure.story('Атрибута нет в группе')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52942")
    @pytest.mark.defect  # https://git.dev-mcx.ru/zenit/profile-service/-/issues/57
    @pytest.mark.xfail
    def test_c52942_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52942")
        logging.info("Удалить список атрибутов из группы. Атрибута нет в группе")
        
        # Номер итерации для генерации данных
        i = 3
        
        # Вызов функции создания группы
        group_gen_delete_name = gen_del_group(profile_api, i)
        
        body = {
            "attrNames": [f"{additional_attribute_name_wrong}"]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.delete(
                f"group/{group_gen_delete_name}/attributes", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_gen_delete_name}' and attr_name = '{additional_attribute_name_wrong}'")
        
        with allure.step("Проверяем количество необходимых записей в БД"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"Количество необходимых записей в БД больше нужного"
            
            # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_gen_delete_name}/attributes")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        logging.info(f"Тест завершен успешно.")
    
    ##########################################################################################
    
    @allure.epic("Удалить список атрибутов из группы")
    @allure.feature('Проверка кода 404')
    @allure.story('Несуществующий name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52409")
    def test_c52409_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52409")
        logging.info("Удалить список атрибутов из группы. Несуществующий name")
        
        # Номер итерации для генерации данных
        i = 5
        
        # Функция генерации дополнительного атрибута
        gen_test_add_attribute_id(profile_api, dbCursor, i)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'attr_group_link')
        
        body = {
            "attrNames": [f"{additional_attribute_jsonName_new[i]}"]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.delete(
                f"group/{group_name_wrong}/attributes", headers = headers,
                data = body_json)  # Записываем ответ метода POST в переменную response
        
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert response.status_code == 404, f"Код ответа не совпадает с ожидаемым! " \
                                                f"Ожидаемый код ответа: 404, полученный: {response.status_code}"  # Проверка кода ответа
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_name_wrong}' and attr_name = '{additional_attribute_jsonName_new[i]}'")
        
        with allure.step("Проверяем количество необходимых записей в БД"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"Количество необходимых записей в БД больше нужного"
            
            # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name_wrong}/attributes")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_after = count_record_db(dbCursor, 'attr_group_link')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса верное")
        
        logging.info(f"Тест завершен успешно.")
