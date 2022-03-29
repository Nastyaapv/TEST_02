import logging
import requests
import psycopg2
import pytest
import os
import http.client  # импорт библиотеки http
from myconfig import *  # импорт переменных из файла

# global timestamp
timestamp = datetime.strftime(datetime.now(), "%d-%m-%Y_%H-%M-%S")  # Определение формата даты и времени
# global timestamp_day
timestamp_day = datetime.strftime(datetime.now(), "%d-%m-%Y")  # Определение формата даты и времени
if not os.path.exists('logs'):  # Если нет папки logs
    os.makedirs('logs')  # Создать папку logs

if not os.path.exists('logs/' + 'conftest'):  # Если нет папки conftest
    os.makedirs('logs/' + 'conftest')  # Создать папку conftest

if not os.path.exists('logs/' + 'conftest/' + timestamp_day):  # Если нет сегодняшней папки
    os.makedirs('logs/' + 'conftest/' + timestamp_day)  # Создать сегодняшнюю папку

logging.basicConfig(filename = 'logs/' + 'conftest/' + timestamp_day + '/' + timestamp + '.log',
                    filemode = 'a',
                    format = '[%(levelname)s] %(asctime)s - %(message)s (%(filename)s:%(lineno)s)',
                    datefmt = '%Y-%m-%d %H:%M:%S',
                    level = logging.INFO)

global path_log_file  # В гите удалить


# Конфигурационные настройки pytest логирования
@pytest.hookimpl(tryfirst = True)
def pytest_configure(config):
    config._metadata = None  # Очистить данные окружения
    if not os.path.exists('logs'):  # Если нет папки logs
        os.makedirs('logs')  # Создать папку logs
    
    if not os.path.exists('logs/' + 'test_run'):  # Если нет папки test_run
        os.makedirs('logs/' + 'test_run')  # Создать test_run папку
    
    if not os.path.exists('logs/' + 'test_run/' + timestamp_day):  # Если нет сегодняшней папки
        os.makedirs('logs/' + 'test_run/' + timestamp_day)  # Создать сегодняшнюю папку
    
    if not config.option.log_file:  # Если в конфигурационном файле pytest.ini не указан параметр log_file
        config.option.log_file = 'logs/' + 'test_run/' + timestamp_day + '/' + timestamp + '.log'  # Формирование пути к log-файлу
        


# Проверка подключения к VPN
def vpn_connection():
    try:
        connection = http.client.HTTPConnection(f"{URL_SERVER}:{URL_PORT}")
        connection.request("GET", "/")
        connection.getresponse()
        # logging.critical("VPN connection is settled")
        vpn_conn = True
    except OSError:
        vpn_conn = False
        logging.warning("VPN connection error")
        logging.debug("Test is not started")
    return vpn_conn


#  Создание курсора для выполнения действий в БД
@pytest.fixture(scope = "class")
def dbCursor(cn):
    try:
        dbCursor = cn.cursor()
        yield dbCursor
    except (Exception, psycopg2.DatabaseError) as error:
        logging.debug("Error in transction Reverting all other operations of a transction ", error)
        cn.rollback()


# Подключение к БД
@pytest.fixture(scope = "class")
def cn():
    cn = psycopg2.connect(user = f"{USER}",  # имя пользователя
                          password = f"{PASSWORD}",  # пароль
                          host = f"{SERVER}",  # хост/сервер
                          port = f"{PORT}",  # порт
                          database = f"{DATABASE}")  # имя БД
    yield cn
    cn.close()



@pytest.fixture
def profile_api():
    return ApiClient(URL)  # записываем в фикстуру общий адрес для всех запросов


# Фикстура возвращает объект с базовым адресом для дальнейших запросов.
# При инициализации объекта класс принимает в себя аргумент url
class ApiClient:
    def __init__(self, url):
        self.url = url
    
    # Добавление в класс метод GET для отправки запросов.
    def get(self, path = "/", params = None, headers = None):  # url, разделитель, параметры, заголовки
        url = f"{self.url}{path}"  # url + разделитель
        return requests.get(url = url, params = params,
                            headers = headers)  # возвращает значение функции с url, параметрами, заголовками
    
    # Добавление в класс метод DELETE для удаления запросов.
    def delete(self, path = "/", params = None, headers = None, data = None):  # url, разделитель, параметры, заголовки
        url = f"{self.url}{path}"  # url + разделитель
        return requests.delete(url = url, params = params,
                               headers = headers,
                               data = data)  # возвращает значение функции с url, параметрами, заголовками
    
    # Добавление в класс метод POST для удаления запросов.
    def post(self, path = "/", params = None, headers = None, data = None,
             files = None):  # url, разделитель, параметры, заголовки
        url = f"{self.url}{path}"  # url + разделитель
        return requests.post(url = url, params = params, headers = headers, data = data,
                             files = files)  # возвращает значение функции с url, параметрами, заголовками
    
    # Добавление в класс метод PUT.
    def put(self, path = "/", params = None, headers = None, data = None,
            files = None):  # url, разделитель, параметры, заголовки
        url = f"{self.url}{path}"  # url + разделитель
        return requests.put(url = url, params = params, headers = headers, data = data,
                            files = files)  # возвращает значение функции с url, параметрами, заголовками
    
    # Добавление в класс метод PATCH.
    def patch(self, path = "/", params = None, headers = None, data = None,
              files = None):  # url, разделитель, параметры, заголовки
        url = f"{self.url}{path}"  # url + разделитель
        return requests.patch(url = url, params = params, headers = headers, data = data,
                              files = files)  # возвращает значение функции с url, параметрами, заголовками
