import allure

from conftest import *
from functions import gen_test_add_attribute_id, parse_response_json, check_response_schema, \
    count_record_db_condition, count_record_db, assert_status_code
from json_schemas import schema_404_error


@allure.epic("Удалить дополнительный атрибут")
@allure.description('Удалить дополнительный атрибут')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test200:
    
    @allure.epic("Удалить дополнительный атрибут")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52192")
    @pytest.mark.smoke
    def test_c52192_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52192")
        logging.info("Удалить дополнительный атрибут. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 4  # Сначала создаем атрибут
        
        # Записываем шаг в отчет allure
        with allure.step(
                f"Создали атрибут c номером итерации в списке переменных additional_attribute_id_<param> - {i}"):
            # Вызов функции генерации
            additional_attribute_id_del = gen_test_add_attribute_id(profile_api, dbCursor, i)[1]
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'additional_attribute')
        
        # Параметры для DELETE метода
        
        # Параметры запроса
        params = {
            "useJsonNameAsId": False
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/additional/{additional_attribute_id_del}", params = params)
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Todo доб. проверку что тело ответа пустое
        
        # Вызываем GET метод, для проверки того, что данные удалились
        # Параметры для GET метода
        # Вызываем метод получения доп. атрибута для проверки того, что данные удалились
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_del}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 404)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  schema_404_error)  # Проверка JSON-схемы ответа
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f" id = '{additional_attribute_id_del}'")
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'additional_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before - 1 == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.debug(f"Количество записей в БД после выполнения запроса верное")
            logging.info(f"В БД удалилась 1 запись.")
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД удалилась запись. "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД не удалилась запись "
        
        logging.info(f"Тест завершен успешно.")
    
    ###########################################################################################################################################
    
    @allure.epic("Удалить дополнительный атрибут")
    @allure.feature('Проверка кода 200')
    @allure.story('Использовать jsonName в качестве идентификатора')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/55339")
    def test_c55339_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/55339")
        logging.info("Удалить дополнительный атрибут. Использовать jsonName в качестве идентификатора")
        
        i = 4  # Сначала создаем атрибут
        additional_attribute_id_del = gen_test_add_attribute_id(profile_api, dbCursor, i)[1]
        
        # Получаем количество записей в БД
        count_record_db_before = count_record_db(dbCursor, 'additional_attribute')
        
        params = {
            "useJsonNameAsId": True
        }
        
        # Отправляем запрос
        response = profile_api.delete(
                f"/profile/attributes/additional/{additional_attribute_jsonName_new[i]}",
                params = params)  # Записываем ответ метода в переменную response
        
        # Todo доб. проверку что тело ответа пустое
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Вызываем метод получения доп. атрибута для проверки того, что данные создались
        response = profile_api.get(
                f"/profile/attributes/additional/{additional_attribute_id_del}")  # Записываем ответ метода GET в переменную response
        
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
        count_record_db_after = count_record_db(dbCursor, 'additional_attribute')
        
        # Получаем количество записей в БД по условию
        count_record_db_cond = count_record_db_condition(dbCursor, 'additional_attribute',
                                                         f" json_name = '{additional_attribute_jsonName_new[i]}'")
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД нет удаляемой записи "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 0, f"В БД не удалилась запись"
            logging.debug(f"В БД удалилась запись.")
        
        with allure.step("Проверка того, что в БД удалилась 1 запись"):  # Записываем шаг в отчет allure
            assert count_record_db_before - 1 == count_record_db_after, f"В БД удалилось не верное кол-во записей"
            logging.info(f"В БД удалилась только 1 запись.")
        logging.info(f"Тест завершен успешно.")
