import jmespath
import allure

from conftest import *
from json_schemas import GET_group_200_main_schema
from functions import check_response_schema, parse_response_json, \
    assert_status_code, \
    reformatted_param, params_record_db_condition, count_record_db_condition, gen_group


@allure.epic("Получить данные о группе")
@allure.description('Получить данные о группе')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test200:
    
    @allure.epic("Получить данные о группе")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52391")
    @pytest.mark.smoke
    def test_c52391_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52391")
        logging.info("Получить данные о группе. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 0
        
        # Вызов функции для создания группы
        group_name = gen_group(profile_api, i)
        
        # Получаем количество записей в БД
        count_record_db_condition(dbCursor, 'attr_group', f"name = '{group_name}'")
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, GET_group_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            list_len = len(param_ALL_group)  # считаем длину списка
            # Сверяем все строки из файла
            for y in range(list_len):
                json_value = jmespath.search(f"{param_ALL_group[y]}",
                                             response_json)  # Ищем каждый параметр из файла с параметрами json
                
                # Если параметр = metadata и creationDate, то выполняется доп. обработка поля, если иные поля, то значение остается таким же
                json_value = reformatted_param(param_ALL_group[y], json_value)
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_group[y], "attr_group",
                                                      f"name = '{group_name}' ORDER BY id ASC")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_ALL_group[y]} = {db_query}.\n" \
                                               f"Значение в json {param_ALL_group[y]} = {json_value}.\n"
                
                logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")
        
        logging.info(f"Тест завершен успешно.")
