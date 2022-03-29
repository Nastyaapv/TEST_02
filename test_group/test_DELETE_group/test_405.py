import allure

from conftest import *
from functions import count_record_db


@allure.epic("Удалить группу")
@allure.description('Удалить группу')
@pytest.mark.skipif(vpn_connection is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.group
class Test405:
    
    @allure.epic("Удалить группу")
    @allure.feature('Проверка кода 404')
    @allure.story('Не указывать name')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52376")
    def test_c52376_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52376")
        logging.info("Удалить группу. Не указывать name")
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_before = count_record_db(dbCursor, 'attr_group')
        
        # Отправляем запрос
        response = profile_api.delete(
                f"group/")  # Записываем ответ метода POST в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            from functions import assert_status_code
            assert_status_code(response, 405)
        
        # Получаем количество записей в БД до выполнения запроса
        count_record_after = count_record_db(dbCursor, 'attr_group')
        
        # Сверка количества записей в БД и в теле ответа
        with allure.step("Сверка количество записей в БД до и после"):  # Записываем шаг в отчет allure
            assert count_record_before == count_record_after, f"Количество записей до  {count_record_before}, после: {count_record_after}"
            logging.info(f"Количество записей в БД после выполнения запроса верное")
        logging.info(f"Тест завершен успешно.")
