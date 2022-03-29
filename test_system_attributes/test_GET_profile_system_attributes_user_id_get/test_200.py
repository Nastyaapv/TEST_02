import allure
import jmespath

from conftest import *
from functions import gen_user_system_attributes, parse_response_json, assert_status_code, check_response_schema, \
    params_record_db_condition
from json_schemas import GET_profile_system_attributes_user_200_main_schema


@allure.epic("Получение значений системных атрибутов для указанного пользователя")
@allure.description('Получение значений системных атрибутов для указанного пользователя')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test200:
    
    @allure.epic("Получение значений системных атрибутов для указанного пользователя")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52196")
    @pytest.mark.xfail  # https://git.dev-mcx.ru/zenit/profile-service/-/issues/188
    @pytest.mark.smoke
    def test_c52196_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52196")
        logging.info("Получение значений системных атрибутов для указанного пользователя. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 2
        
        # Вызов функции поиска заполненных или генерация заполнения значений системных атрибутов
        system_attributes_user_id = gen_user_system_attributes(profile_api, dbCursor, i)[0]
        
        response = profile_api.get(
                f"profile/system-attributes/user/{system_attributes_user_id}/get")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
            
            # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json,
                                  GET_profile_system_attributes_user_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(response_json)
        logging.debug(f"Количество json объектов = {count_json}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            j = 0
        # Сверяем все строки из файла
        while j < count_json:  # До прохождения всех json ключей
            json_name_system_attribute = jmespath.search(f"keys(@) | [{j}]",
                                                         response_json)  # Ищем каждый параметр из файла с параметрами json
            json_value = jmespath.search(f"{json_name_system_attribute}",
                                         response_json)  # Ищем каждый параметр из файла с параметрами json
            if json_value != '':
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_user_system_attribute,
                                                      "user_system_attribute",
                                                      f"user_id = '{system_attributes_user_id}' and name = '{json_name_system_attribute}'")
                
                logging.debug(f"Параметр в БД {param_ALL_user_system_attribute} = {db_query}.")
                logging.debug(f"Значение в json {param_ALL_user_system_attribute} = {json_value}.")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_user_system_attribute} = {db_query}.\n" \
                                               f"Значение в json {param_ALL_user_system_attribute} = {json_value}.\n"
            else:
                assert json_value == "", "Значение заполнено в БД."
            j += 1
        
        logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        logging.info(f"Тест завершен успешно.")
