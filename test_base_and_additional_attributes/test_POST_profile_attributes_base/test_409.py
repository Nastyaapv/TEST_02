import allure
import jmespath

from conftest import *
from functions import count_record_db, count_record_db_condition, parse_response_json, \
    parse_request_json, gen_test_base_attribute_id, assert_status_code, reformatted_param, params_record_db_condition


@allure.epic("Добавить базовый атрибут")
@allure.description('Добавить базовый атрибут')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.base_and_additional_attributes
class Test409:
    
    @allure.epic("Добавить базовый атрибут")
    @allure.feature('Проверка кода 409')
    @allure.story('Базовый атрибут уже существует по jsonName')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52157")
    def test_c52157_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52157")
        logging.info("Добавить базовый атрибут. Базовый атрибут уже существует по jsonName")
        
        # Номер итерации для генерации данных
        i = 0  # Для списков base_attribute_<...>_new
        
        # Сначала создаем данные, что бы они потом показались существующими
        gen_test_base_attribute_id(profile_api, dbCursor, i)
        
        # Получаем значения атрибута, и проверяем что они потом не изменятся
        params = {
            "useJsonNameAsId": True
        }
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_json_name_new[i]}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответ
        response_json_before, response_json_beautifully = parse_response_json(response)  # Парсинг тела ответа
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'base_attribute')
        
        # Номер итерации для генерации данных
        j = 2  # Для списков base_attribute_<...>_new
        
        # json_name используем старое значение, уже созданное
        body = {
            "identity": f"{base_attribute_identity_new[j]}",
            "name": f"{base_attribute_name_new[j]}",
            "jsonName": f"{base_attribute_json_name_new[i]}",  # Тут используем старое значение, уже созданное
            "type": base_attribute_type_new[j],
            "metadata": base_attribute_metadata_new[j],
            "deleted": base_attribute_deleted_new[j]
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
            assert_status_code(response, 409)
        
        # Получаем количество записей в БД по условию
        # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
        count_record_db_cond = count_record_db_condition(dbCursor, 'base_attribute',
                                                         f"name = '{base_attribute_name_new[i]}' and json_name = '{base_attribute_json_name_new[i]}'")
        
        # Проверяем наличие в БД по условию
        with allure.step("Проверка того, что в БД есть запись "):  # Записываем шаг в отчет allure
            assert count_record_db_cond == 1, f"В БД больше одной или вообще нет записей "
            logging.debug(f"В БД уже есть запись.")
        
        params = {
            "useJsonNameAsId": True
        }
        response = profile_api.get(
                f"/profile/attributes/base/{base_attribute_json_name_new[i]}",
                params = params)  # Записываем ответ метода GET в переменную response
        
        response_json_after, response_json_beautifully = parse_response_json(response)  # Парсинг тела ответа
        
        with allure.step("Проверка что данные до и после выполнения запроса добавления - одинаковые"):
            assert response_json_before == response_json_after, f'Данные до: {response_json_before}' \
                                                                f'Данные после: {response_json_after}'
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            # Сверяем все строки из файла
            for key in param_ALL_base_attribute:
                json_value = jmespath.search(f"{key}",
                                             response_json_after)  # Ищем каждый параметр из файла с параметрами json
                
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
            assert count_record_before == count_record_after, f"Количество записей до {count_record_before}, после: {count_record_after}"
            logging.debug(f"Количество записей в БД после выполнения запроса не изменилось")
        logging.info(f"Тест завершен успешно.")
