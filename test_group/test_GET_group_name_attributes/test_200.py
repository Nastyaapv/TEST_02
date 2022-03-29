import allure
import jmespath

from conftest import *
from functions import parse_response_json, assert_status_code, check_response_schema, params_record_db_condition, \
    count_record_db_condition, gen_group, gen_add_attr_del_group
from json_schemas import GET_group_link_200_main_schema


@allure.epic("Получить список атрибутов входящих в группу")
@allure.description('Получить список атрибутов входящих в группу')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test200:
    
    @allure.epic("Получить список атрибутов входящих в группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52377")
    @pytest.mark.smoke
    def test_c52377_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52377")
        logging.info("Получить список атрибутов входящих в группу. Прямой сценарий")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Вызов функции создания группы
        group_name = gen_group(profile_api, i)
        
        # Вызов функции добавления атрибутов в группу, без удаления
        gen_add_attr_del_group(profile_api, dbCursor, group_name)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_name}' and block = '{group_gen_del_block}'")
        
        params = {
            "block": f"{group_gen_del_block}"
        }
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_name}/attributes", params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, GET_group_link_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for y in range(count_record):  # цикл по содержимому БД
                # Сверяем все строки из файла в БД и json
                for key in param_ALL_group_link:
                    json_value = jmespath.search(f"[{y}].{key}",
                                                 response_json)  # Ищем каждый параметр json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_group_link[key],
                                                          f"(SELECT ROW_NUMBER () OVER (ORDER BY attr_group.id), {param_ALL_group_link[key]} FROM attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id "
                                                          f"WHERE name = '{group_name}')x",
                                                          f"ROW_NUMBER = {y + 1}")
                    
                    logging.debug(f'Параметр в БД - {param_ALL_group_link[key]} - значение {db_query}')
                    logging.debug(f'Параметр в json - {key} - значение {json_value}')
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f" Данные поля не совпадают для этого name = {group_name}!\n" \
                                                   f"Параметр в БД {param_ALL_group_link[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество записей: {count_record}, после: {count_json}"
            logging.debug(f"Количество записей в БД = {count_record}")
            logging.debug(f"Количество записей в json = {count_json}")
            logging.info(f"Количество записей в БД и json объектов совпадает")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получить список атрибутов входящих в группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Несуществующий block')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52923")
    def test_c52923_main(self, profile_api, cn, dbCursor):
        logging.info(
                "Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52923")
        logging.info("Получить список атрибутов входящих в группу. Несуществующий block")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_db_condition(dbCursor,
                                  'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                  f"name = '{group_gen_name[i]}' and block = '{group_block_wrong}'")
        
        params = {"block": f"{group_block_wrong}"}
        
        # Указываем данные запроса
        response = profile_api.get(
                f"/group/{group_gen_name[i]}/attributes",
                params = params)  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, GET_group_link_200_main_schema)  # Проверка JSON-схемы ответа
        
        with allure.step("Проверка что данных нет в БД"):
            # Получаем количество записей в БД до выполнения запроса
            db_query = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_gen_name[i]}' and block = '{group_block_wrong}'")
            
            assert db_query == 0, f"Количество записей в БД - {db_query}.\n" \
                                  f"Ожидаемое количество записей в БД - 0.\n"
        
        logging.info(f"Данных нет в БД. Кейс успешный.")
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получить список атрибутов входящих в группу")
    @allure.feature('Проверка кода 200')
    @allure.story('Не указан block')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52406")
    def test_c52406_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52406")
        logging.info("Получить список атрибутов входящих в группу. Не указан block")
        
        # Номер итерации для генерации данных
        i = 1
        
        # Получаем количество записей в БД по условию
        count_record = count_record_db_condition(dbCursor,
                                                 'attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id',
                                                 f"name = '{group_gen_name[i]}'")
        
        # Отправляем запрос
        response = profile_api.get(
                f"/group/{group_gen_name[i]}/attributes")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, GET_group_link_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            for y in range(count_record):  # цикл по содержимому БД
                # Сверяем все строки из файла в БД и json
                for key in param_ALL_group_link:
                    json_value = jmespath.search(f"[{y}].{key}",
                                                 response_json)  # Ищем каждый параметр json
                    
                    # Получаем параметр в БД условию
                    db_query = params_record_db_condition(dbCursor, param_ALL_group_link[key],
                                                          f"(SELECT ROW_NUMBER () OVER (ORDER BY attr_group.id), {param_ALL_group_link[key]} FROM attr_group_link JOIN attr_group ON attr_group_link.group_id = attr_group.id "
                                                          f"WHERE name = '{group_gen_name[i]}')x",
                                                          f"ROW_NUMBER = {y + 1}")
                    
                    logging.debug(f'Параметр в БД - {param_ALL_group_link[key]} - значение {db_query}')
                    logging.debug(f'Параметр в json - {key} - значение {json_value}')
                    
                    # Сверяем данные параметра json и ячейки БД
                    assert db_query == json_value, f" Данные поля не совпадают для этого name = {group_gen_name[i]}!\n" \
                                                   f"Параметр в БД {param_ALL_group_link[key]} = {db_query}.\n" \
                                                   f"Значение в json {key} = {json_value}.\n"
            logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество записей: {count_record}, после: {count_json}"
            logging.debug(f"Количество записей в БД = {count_record}")
            logging.debug(f"Количество записей в json = {count_json}")
            logging.info(f"Количество записей в БД и json объектов совпадает")
        logging.info(f"Тест завершен успешно.")
