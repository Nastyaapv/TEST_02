import allure

from conftest import *
from functions import parse_request_json, check_response_schema, parse_response_json, \
    assert_status_code, count_record_db_condition, count_record_db, gen_del_group, gen_add_attr_del_group

from json_schemas import schema_empty_json


@allure.epic("Удалить список атрибутов из группы")
@allure.description('Удалить список атрибутов из группы')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test200:
    
    @allure.epic("Удалить список атрибутов из группы")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52408")
    @pytest.mark.smoke
    def test_c52408_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52408")
        logging.info("Удалить список атрибутов из группы. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции создания группы
        group_gen_delete_name = gen_del_group(profile_api, i)
        
        # Вызов функции добавления атрибутов в группу, для их удаления из группы
        group_gen_attr_name = gen_add_attr_del_group(profile_api, dbCursor, group_gen_del_name)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'attr_group_link')
        
        body = {
            "attrNames": [
                f"{group_gen_attr_name}"
            ]
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
            assert_status_code(response, 200)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_gen_delete_name}' and attr_name = '{group_gen_attr_name}'")
        
        with allure.step("Проверим что количество записей БД = 0"):  # Записываем шаг в отчет allure
            assert count_record == 0, f"Код ответа не совпадает с ожидаемым! "
            logging.info(f"В БД удалилась запись.")
            
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
            check_response_schema(response_json, schema_empty_json)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_after = count_record_db(dbCursor, 'attr_group_link')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before - 1 == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.debug(f"Количество записей в БД после выполнения запроса верное")
        logging.info(f"Тест завершен успешно.")
