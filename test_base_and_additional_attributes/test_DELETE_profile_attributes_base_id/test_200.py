import allure

from conftest import *
from functions import parse_response_json, check_response_schema, \
    count_record_db_condition, gen_test_base_attribute_id, count_record_db, assert_status_code
from json_schemas import schema_404_error


@allure.epic("Удалить базовый атрибут")
@allure.description('Удалить базовый атрибут')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test200:
    
    @allure.epic("Удалить базовый атрибут")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/54672")
    @pytest.mark.smoke
    def test_c54672_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/54672")
        logging.info("Удалить базовый атрибут. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 4  # Сначала создаем атрибут
        # Вызов функции генерации base attribute ID
        base_attribute_id_del = gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Получаем количество записей в БД
        count_record_db_before = count_record_db(dbCursor, 'base_attribute')
        
        params = {
            "useJsonNameAsId": False
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/base/{base_attribute_id_del}", params = params)
        
        # Todo доб. проверку что тело ответа пустое
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные удалились
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_id_del}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД
        count_record_db_after = count_record_db(dbCursor, 'base_attribute')
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f" id = '{base_attribute_id_del}'")
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_db_before - 1 == count_record_db_after, f"Количество записей до  {count_record_db_before}, после: {count_record_db_after}"
            logging.debug(f"Количество записей в БД после выполнения запроса верное")
            logging.info(f"В БД удалилась 1 запись.")
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД удалилась запись. "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД не удалилась запись "
        logging.info(f"Тест завершен успешно.")
    
    #########################################################################################
    
    @allure.epic("Удалить базовый атрибут")
    @allure.feature('Проверка кода 200')
    @allure.story('Использовать jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55352")
    def test_c55352_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55352")
        logging.info("Удалить базовый атрибут. Использовать jsonName в качестве идентификатора")
        
        # Номер итерации для генерации данных
        i = 4  # Сначала создаем атрибут
        # Вызов функции генерации base attribute ID
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Получаем количество записей в БД
        count_record_db_before = count_record_db(dbCursor, 'base_attribute')
        
        params = {
            "useJsonNameAsId": True
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/base/{base_attribute_json_name_new[i]}", params = params)
        
        # Todo доб. проверку что тело ответа пустое
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        params = {
            "useJsonNameAsId": True
        }
        # Вызываем метод получения доп. атрибута для проверки того, что данные удалились
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_json_name_new[i]}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД
        count_record_db_after = count_record_db(dbCursor, 'base_attribute')
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f" json_name = '{base_attribute_json_name_new[i]}'")
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД нет удаляемой записи "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД не удалилась запись"
            logging.debug(f"В БД удалилась запись.")
        
        with allure.step("Проверка того, что в БД удалилась 1 запись"):  # Записываем шаг в отчет allure
            assert count_record_db_before - 1 == count_record_db_after, f"В БД удалилось не верное кол-во записей"
            logging.info(f"В БД удалилась только 1 запись.")
        logging.info(f"Тест завершен успешно.")
