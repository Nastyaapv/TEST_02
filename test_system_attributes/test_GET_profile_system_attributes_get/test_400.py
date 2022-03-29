import allure

from conftest import *
from functions import assert_status_code


@allure.epic("Получение системного атрибута по идентификатору")
@allure.description('Получение системного атрибута по идентификатору')
@pytest.mark.skipif(vpn_connection() is False,
                    reason = "VPN connection error")  # В файле conftest.py проверка на подключение к VPN
@pytest.mark.system_attributes
class Test400:
    
    @allure.epic("Получение системного атрибута по идентификатору")
    @allure.feature('Проверка кода 400')
    @allure.story('Указать пустой id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/53366")
    def test_c53366_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/53366")
        logging.info("Получение системного атрибута по идентификатору. Указать пустой id")
        
        params = {"id": f"{empty_value}"}
        response = profile_api.get(f"/profile/system-attributes/get",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Todo схемы нет
        
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получение системного атрибута по идентификатору")
    @allure.feature('Проверка кода 400')
    @allure.story('Не указывать параметр id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52135")
    def test_c52135_main(self, profile_api, cn, dbCursor):
        logging.info(f"Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52135")
        logging.info("Получение системного атрибута по идентификатору. Не указывать параметр id")
        
        # Указываем данные запроса
        response = profile_api.get(
                f"/profile/system-attributes/get/")  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Todo схемы нет
        
        logging.info(f"Тест завершен успешно.")
    
    ################################################################################################################################################################
    
    @allure.epic("Получение системного атрибута по идентификатору")
    @allure.feature('Проверка кода 400')
    @allure.story('Невалидный id')
    @allure.testcase("https://tr.instream.ru:7443/testrail/index.php?/cases/view/52195")
    def test_c52195_main(self, profile_api, cn, dbCursor):
        logging.info("Тест начат. Ссылка на ТК: https://tr.instream.ru:7443/testrail/index.php?/cases/view/52195")
        logging.info("Получение системного атрибута по идентификатору. Невалидный id")
        
        params = {"id": f"{system_attributes_id_wrong}"}
        
        response = profile_api.get("/profile/system-attributes/get",
                                   params = params)  # Записываем ответ метода GET в переменную response
        
        # Вызываем функцию проверки кода ответа
        with allure.step("Запрос отправлен, посмотрим код ответа"):  # Записываем шаг в отчет allure
            assert_status_code(response, 400)
        
        # Todo схемы нет
        
        logging.info(f"Тест завершен успешно.")
    ################################################################################################################################################################
