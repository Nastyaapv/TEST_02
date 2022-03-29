import allure
import jmespath

from functions import check_response_schema, parse_response_json, \
    assert_status_code, \
    params_record_db_condition, count_record_db

from conftest import *
from json_schemas import GET_group_200_main_schema


@allure.epic("Получить список групп")
@allure.description('Получить список групп')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test200:
    
    @allure.epic("Получить список групп")
    @allure.feature('Проверка кода 200')
    @allure.story('Прямой сценарий')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52357")
    @pytest.mark.smoke
    def test_c52357_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52357")
        logging.info("Получить список групп. Прямой сценарий")
        
        # Получаем количество записей в БД
        count_record = count_record_db(dbCursor, 'attr_group')
        
        # Отправляем запрос
        response = profile_api.get(
                "/group")  # Записываем ответ метода GET в переменную response
        
        # Парсинг тела ответа
        response_json = parse_response_json(response)[0]
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 200)
        
        # Проверка JSON-схемы ответа
        with allure.step("Проверка JSON-схемы ответа:"):
            check_response_schema(response_json, GET_group_200_main_schema)  # Проверка JSON-схемы ответа
        
        # Подсчет количества json объектов
        count_json = len(jmespath.search(f"[*]", response_json))
        logging.debug(f"Количество json объектов = {count_json}")
        
        with allure.step("Проверка что отобразились именно необходимые данные"):
            i = 0  # задаем переменную для продвижения по списку содержимого в теле ответа
            j = 0  # задаем переменную для продвижения по списку параметров
        list_len = len(param_ALL_group)  # считаем длину списка
        while i < count_record:  # цикл по содержимому БД
            r_name = jmespath.search(f"[{i}].name", response_json)  # получаем значение id
            # Сверяем все строки из файла в БД и json
            while j < list_len:  # цикл по параметрам
                
                json_value = jmespath.search(f"[{i}].{param_ALL_group[j]}",
                                             response_json)  # Ищем каждый параметр json
                
                # Получаем параметр в БД условию
                db_query = params_record_db_condition(dbCursor, param_ALL_group[
                    j], "attr_group", f"name = '{r_name}' ORDER BY id ASC")
                
                logging.debug(f'Параметр в БД - {param_ALL_group[j]} - значение {db_query}')
                logging.debug(f'Параметр в json - {param_ALL_group[j]} - значение {json_value}')
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f" Данные поля не совпадают для этого name = {r_name}!\n" \
                                               f"Параметр в БД {param_ALL_group[j]} = {db_query}.\n" \
                                               f"Значение в json {param_ALL_group[j]} = {json_value}.\n"
                j = j + 1  # Увеличиваем счетчик
            i = i + 1  # Увеличиваем счетчик
            j = 0
        logging.info(f"JSON-данные тела ответа совпадают с данными в БД.")
        
        with allure.step("Сверка количество записей в БД и json объектов"):  # Записываем шаг в отчет allure
            # Сверка количества записей в БД и в теле ответа
            assert count_json == count_record, f"Количество записей: {count_record}, после: {count_json}"
            logging.debug(f"Количество записей в БД = {count_record}")
            logging.debug(f"Количество записей в json = {count_json}")
            logging.info(f"Количество записей в БД и json объектов совпадает")
        logging.info(f"Тест завершен успешно.")
