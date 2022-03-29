import allure
import jmespath

from conftest import *
from functions import count_record_db, count_record_db_condition, parse_response_json, \
    parse_request_json, assert_status_code, params_record_db_condition, reformatted_param


@allure.epic("Добавить базовый атрибут")
@allure.description('Добавить базовый атрибут')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test201:
    
    @allure.epic("Добавить базовый атрибут")
    @allure.feature('Проверка кода 201')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52154")
    @pytest.mark.smoke
    def test_c52154_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52154")
        logging.info("Добавить базовый атрибут. Прямой сценарий ")
        
        # Номер итерации для генерации данных base_attribute_<param>_new
        i = 5  # Для списка base_attribute_name_new
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'base_attribute')
        
        body = {
            "identity": f"{base_attribute_identity_new[i]}",
            "name": f"{base_attribute_name_new[i]}",
            "jsonName": f"{base_attribute_json_name_new[i]}",
            "type": base_attribute_type_new[i],
            "metadata": base_attribute_metadata_new[i],
            "deleted": base_attribute_deleted_new[i]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        response = profile_api.post("profile/attributes/base", headers = headers,
                                    data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 201)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name = '{base_attribute_name_new[i]}' and json_name = '{base_attribute_json_name_new[i]}'")
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД есть добавляемая запись "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 1, f"В БД больше одной или вообще нет записей "
            logging.debug(f"В БД добавилась запись.")
        
        params = {
            "useJsonNameAsId": True
        }
        
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_json_name_new[i]}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        response_json = parse_response_json(response)[0]  # Парсинг тела ответа
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Функция реформатирования параметров
                json_value = reformatted_param(key, json_value, 'base_attribute')
                
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_ALL_base_attribute[key],
                                                      'base_attribute',
                                                      f"json_name = '{base_attribute_json_name_new[i]}'")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_base_attribute[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        # Получаем количество записей в БД после выполнения запроса
        count_record_after = count_record_db(dbCursor,
                                             'base_attribute')  # Получаем количество записей в БД после выполнения запроса
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before + 1 == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
