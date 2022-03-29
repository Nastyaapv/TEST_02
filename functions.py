import json
import logging
from datetime import timedelta

import jmespath
import jsonschema
from jsonschema.exceptions import ValidationError

from myconfig import *


# Базовые функции для тестов
# Парсинг тела ответа
def parse_response_json(response):
    response_json = response.json()  # Получаем тело ответа в формате json
    response_beautify = json.dumps(response_json, indent = 4, sort_keys = True,
                                   ensure_ascii = False)  # Форматируем json ответ в читабельный вид
    
    logging.debug(f"Тело ответа: \n"
                  f"{response_beautify}")  # Логируем тело ответа
    
    return response_json, response_beautify


# Проверка JSON-схемы ответа
def check_response_schema(response_json, name_schema):
    try:
        jsonschema.validate(response_json, name_schema)
        logging.info(f"JSON-схема тела ответа совпадает с ожидаемой.")
    except ValidationError:
        logging.error(f"JSON-схема ответа не совпадает с ожидаемой!", exc_info = True)
        raise ValidationError


# Парсинг тела запроса
def parse_request_json(body):
    body_json = json.dumps(body)
    body_json_beautifully = json.dumps(body, indent = 4, sort_keys = True,
                                       ensure_ascii = False)
    logging.debug(f"Тело запроса: \n {body_json_beautifully}")
    
    return body_json, body_json_beautifully


# Проверка статус кода ответа
def assert_status_code(response, code):
    try:
        assert response.status_code == code, f"Код ответа не совпадает с ожидаемым! " \
                                             f"Ожидаемый код ответа: {code}, полученный: {response.status_code}"  # Проверка кода ответа
        logging.info(f"Код ответа - {code}. Верно.")
    except AssertionError:
        logging.info(f"Тест упал.")
        logging.info(f"Проверка не прошла, выводим тело ответа сразу.")
        parse_response_json(response)
        assert response.status_code == code  # Для того что бы тест пометился упавшим


# Получаем количество записей в БД
def count_record_db(dbCursor, table):
    # Получаем количество записей в БД
    query_count = f"SELECT COUNT(*) FROM {table}"
    dbCursor.execute(query_count)
    count_record = dbCursor.fetchone()[0]
    
    return count_record


# Получаем количество записей в БД по условию
def count_record_db_condition(dbCursor, table, condition):
    query_count = f"SELECT COUNT(*) FROM {table} " \
                  f"WHERE {condition}"
    dbCursor.execute(query_count)
    count_record_condition = dbCursor.fetchone()[0]
    
    return count_record_condition


# Получаем значение записи в БД по условию
def params_record_db_condition(dbCursor, params, table, condition):
    query_params = f"SELECT {params} FROM {table} " \
                   f"WHERE {condition}"
    dbCursor.execute(query_params)
    
    params_condition = dbCursor.fetchone()[0]
    
    return params_condition


# Получаем несколько значений записей в БД по условию
def params_record_db_condition_many(dbCursor, params, table, condition):
    query_params = f"SELECT {params} FROM {table} " \
                   f"WHERE {condition}"
    dbCursor.execute(query_params)
    params_condition = dbCursor.fetchone()
    
    return params_condition


# Получаем значение записей в БД без условий
def params_record_db_without_condition(dbCursor, params, table):
    query_params = f"SELECT {params} FROM {table}"
    dbCursor.execute(query_params)
    params_condition = dbCursor.fetchone()[0]
    
    return params_condition


# Функция реформатирования параметров
def reformatted_param(param, value, table = None):
    if param == 'metadata' and value is not None:
        formatted = str(value).replace(" ", "").replace("'", '"')
    
    elif param == 'creationDate':
        #  Преобразуем дату и меняем таймзону
        if table == 'base_attribute':
            formatted = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f+00:00") + timedelta(hours = 3)
        else:
            formatted = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")  # timedelta(hours = 3)
    elif param == 'statusDate':
        formatted = datetime.date(value)
    else:
        formatted = value
    
    return formatted


# Функция подсчета значения size на странице, исходя из кол-ва записей в БД
def record_size_pages(db_count_record):
    size_dict = {0: 10, 10: 25, 25: 50, 51: 100, 101: 200, 201: 300, 301: 400}
    size = None
    for key in size_dict:
        if key <= db_count_record <= size_dict[key]:
            size = size_dict[key]
    
    return size


# Проверка тела ответа с pageable схемой
def check_param_schema(page, size_pages, params_dict, response_json, sort = None, elements = None):
    """
    Описание параметров:
    page - номер страницы.
    size_pages - размер страницы.
    params_dict - словарь из которого берутся ключи для сверки.
    response_json - тело ответа с которым будем сверять params_dict ключи.
    Sort - параметр сортировки, по умолчанию - None.
    Elements - количество элементов в БД по необходимому условию, по умолчанию - None.
    """
    for key in params_dict:
        if key == 'empty':
            # Тут считаем, пустой ли список content - [] или не пустой
            count_objects = len(jmespath.search(f"content[*]", response_json))
            
            # Если count_objects - истина, то - False, иначе True | если count_objects = 1, то False, если count_objects = 0, то True
            expected_empty = False if count_objects else True
            
            # Получаем значение empty из response_json
            actual_empty = jmespath.search(key, response_json)
            
            logging.debug(f'Ожидаемый параметр {key} - {expected_empty} для кол-ва объектов - {count_objects}')
            logging.debug(f'Актуальный параметр {key} - {actual_empty} для кол-ва объектов - {count_objects}')
            
            assert expected_empty == actual_empty, "Параметр empty неправильный."
        
        if key == 'first':
            # Если page - истина, то False, иначе - True | если page = 1, то False, если page = 0, то True
            expected_first = False if page else True
            
            # Получаем значение first из response_json
            actual_first = jmespath.search(key, response_json)
            
            logging.debug(f'Ожидаемый параметр {key} - {expected_first} для страницы - {page}')
            logging.debug(f'Актуальный параметр {key} - {actual_first} для страницы - {page}')
            
            assert expected_first == actual_first, "Параметр first неправильный."
        
        if key == 'last':
            # Тут считаем кол-во объектов content
            count_objects = len(jmespath.search(f"content[*]", response_json))
            
            # Если количество объектов меньше страницы (т.к. подсчет начинается с 1, а size_pages начинается с 0),
            # То страница считается последней
            if count_objects < size_pages:
                expected_last = True
            else:
                expected_last = False
            
            # Получаем значение last из response_json
            actual_last = jmespath.search(key, response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {key} - {expected_last} для размера страницы - {size_pages} и {count_objects} количества объектов на странице')
            logging.debug(
                    f'Актуальный параметр {key} - {actual_last} для размера страницы - {size_pages} и {count_objects} количества объектов на странице')
            
            assert expected_last == actual_last, "Параметр last неправильный."
        
        if key == 'number':
            expected_number = page
            
            # Получаем значение number из response_json
            actual_number = jmespath.search(key, response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {key} - {expected_number} № страницы - {page}')
            logging.debug(
                    f'Актуальный параметр {key} - {actual_number} № страницы - {page}')
            
            assert expected_number == actual_number, "Параметр number неправильный."
        
        if key == 'size':
            expected_size = size_pages
            
            # Получаем значение size из response_json
            actual_size = jmespath.search(key, response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {key} - {expected_size} для размера страницы - {size_pages}')
            logging.debug(
                    f'Актуальный параметр {key} - {actual_size} для размера страницы - {size_pages}')
            
            assert expected_size == actual_size, "Параметр size неправильный."
        
        if key == 'totalPages':
            # Если количество элементов не указано, то считается что кол-во элементов равно размеру size-pages
            if elements is None:
                # Тут считаем кол-во объектов content
                count_objects = len(jmespath.search(f"content[*]", response_json))
            else:
                count_objects = elements
            
            expected_total_pages = None
            
            # Если количество объектов меньше страницы (т.к. подсчет начинается с 1, а size_pages начинается с 0).
            # То страница считается единственной.
            if count_objects <= size_pages and count_objects != 0:
                expected_total_pages = 1
            elif count_objects == 0:
                expected_total_pages = 0
            elif (count_objects % size_pages) != 0:  # если размер списка делится на размер страницы с остатком
                expected_total_pages = (count_objects // size_pages) + 1
            elif (count_objects % size_pages) == 0:
                expected_total_pages = count_objects // size_pages
            
            # Получаем значение size из response_json
            actual_total_pages = jmespath.search(key, response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {key} - {expected_total_pages} для кол-ва записей {count_objects} и размера страницы - {size_pages}')
            logging.debug(
                    f'Актуальный параметр {key} - {actual_total_pages}  для кол-ва записей {count_objects} и размера страницы - {size_pages}')
            
            assert expected_total_pages == actual_total_pages, "Параметр totalPages неправильный."
        
        if key == 'totalElements':
            # Если количество элементов не указано, то считается что кол-во элементов равно размеру size-pages
            if elements is None:
                # Тут считаем кол-во объектов content
                expected_total_elements = len(jmespath.search(f"content[*]", response_json))
            else:
                expected_total_elements = elements
            
            # Получаем значение size из response_json
            actual_total_elements = jmespath.search(key, response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {key} - {expected_total_elements} для кол-ва записей {elements}')
            logging.debug(
                    f'Актуальный параметр {key} - {actual_total_elements}  для кол-ва записей {elements}')
            
            assert expected_total_elements == actual_total_elements, "Параметр totalElements неправильный."
        
        #  Определяет количество элементов массива, используемых для заполнения списочной части элементов управления ComboBox или ListBox. Доступно как в design, так и в run time.
        if key == 'numberOfElements':
            # Тут считаем кол-во объектов content
            expected_number_of_elements = len(jmespath.search(f"content[*]", response_json))
            
            # Получаем значение size из response_json
            actual_number_of_elements = jmespath.search(key, response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {key} - {expected_number_of_elements} для кол-ва записей {elements}')
            logging.debug(
                    f'Актуальный параметр {key} - {actual_number_of_elements}  для кол-ва записей {elements}')
            
            assert expected_number_of_elements == actual_number_of_elements, "Параметр totalElements неправильный."
    
    for key in params_dict.get('sort'):
        
        if key == 'empty':
            # Если sort - истина, то - False, иначе True
            expected_empty = False if sort is not None else True
            
            # Получаем значение empty из response_json
            actual_empty = jmespath.search(f"sort.{key}", response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"sort." + key} - {expected_empty} для кол-ва объектов - {elements}')
            logging.debug(
                    f'Актуальный параметр {"sort." + key} - {actual_empty} для кол-ва объектов - {elements}')
            
            assert expected_empty == actual_empty, "Параметр empty неправильный."
        
        if key == 'sorted':
            # # Если поле сортировки заполнялось, то истина, иначе - ложь
            expected_sorted = True if sort is not None else False
            
            # Получаем значение empty из response_json
            actual_sorted = jmespath.search(f"sort.{key}", response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"sort." + key} - {expected_sorted} для сортировки - {sort}')
            logging.debug(
                    f'Актуальный параметр {"sort." + key} - {actual_sorted} для сортировки - {sort}')
            
            assert expected_sorted == actual_sorted, "Параметр empty неправильный."
        
        if key == 'unsorted':
            # # Если поле сортировки заполнялось, то истина, иначе - ложь
            expected_unsorted = True if sort is None else False
            
            # Получаем значение empty из response_json
            actual_unsorted = jmespath.search(f"sort.{key}", response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"sort." + key} - {expected_unsorted} для сортировки - {sort}')
            logging.debug(
                    f'Актуальный параметр {"sort." + key} - {actual_unsorted} для сортировки - {sort}')
            
            assert expected_unsorted == actual_unsorted, "Параметр empty неправильный."
    
    for key in params_dict.get('pageable'):
        if key == 'pageNumber':
            expected_page_number = page
            
            # Получаем значение number из response_json
            actual_page_number = jmespath.search(f'pageable.{key}', response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"pageable." + key} - {expected_page_number} № страницы - {page}')
            logging.debug(
                    f'Актуальный параметр {"pageable." + key} - {actual_page_number} № страницы - {page}')
            
            assert expected_page_number == actual_page_number, "Параметр pageNumber неправильный."
        
        if key == 'pageSize':
            expected_pagesize = size_pages
            
            # Получаем значение size из response_json
            actual_pagesize = jmespath.search(f'pageable.{key}', response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"pageable." + key} - {expected_pagesize} для размера страницы - {size_pages}')
            logging.debug(
                    f'Актуальный параметр {"pageable." + key} - {actual_pagesize} для размера страницы - {size_pages}')
            
            assert expected_pagesize == actual_pagesize, "Параметр pageSize неправильный."
        
        # Значение, указывающее, содержит ли текущий Pageable элемент информацию о разбиении на страницы.
        if key == 'paged':
            expected_paged = True
            
            # Получаем значение size из response_json
            actual_paged = jmespath.search(f'pageable.{key}', response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"pageable." + key} - {expected_paged} для размера страницы - {size_pages}')
            logging.debug(
                    f'Актуальный параметр {"pageable." + key} - {actual_paged} для размера страницы - {size_pages}')
            
            assert expected_paged == actual_paged, "Параметр paged неправильный."  # Вообще не знаю что это
        
        # Возвращает значение, представляющий отсутствие настройки разбиения на страницы.
        if key == 'unpaged':
            expected_unpaged = False
            
            # Получаем значение size из response_json
            actual_unpaged = jmespath.search(f'pageable.{key}', response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"pageable." + key} - {expected_unpaged} для размера страницы - {size_pages}')
            logging.debug(
                    f'Актуальный параметр {"pageable." + key} - {actual_unpaged} для размера страницы - {size_pages}')
            
            assert expected_unpaged == actual_unpaged, "Параметр unpaged неправильный."  # Вообще не знаю что это
        
        # Возвращает смещение, которое должно быть взято в соответствии с базовой страницей и размером страницы.
        if key == 'offset':
            # Тут считаем кол-во объектов content
            count_objects = len(jmespath.search(f"content[*]", response_json))
            # Если количество объектов меньше страницы (т.к. подсчет начинается с 1, а size_pages начинается с 0),
            # То страница считается единственной
            if count_objects < size_pages:
                expected_offset = 0
            else:
                expected_offset = page * size_pages
            
            # Получаем значение number из response_json
            actual_offset = jmespath.search(f'pageable.{key}', response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"pageable." + key} - {expected_offset} № страницы - {page}')
            logging.debug(
                    f'Актуальный параметр {"pageable." + key} - {actual_offset} № страницы - {page}')
            
            assert expected_offset == actual_offset, "Параметр offset неправильный."
    
    for key in params_dict.get('pageable').get('sort'):
        
        if key == 'empty':
            # Если sort - истина, то - False, иначе True
            expected_empty = False if sort is not None else True
            
            # Получаем значение empty из response_json
            actual_empty = jmespath.search(f"pageable.sort.{key}", response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"pageable.sort." + key} - {expected_empty} для кол-ва объектов - {elements}')
            logging.debug(
                    f'Актуальный параметр {"pageable.sort." + key} - {actual_empty} для кол-ва объектов - {elements}')
            
            assert expected_empty == actual_empty, "Параметр empty неправильный."
        
        if key == 'sorted':
            # # Если поле сортировки заполнялось, то истина, иначе - ложь
            expected_sorted = True if sort is not None else False
            
            # Получаем значение empty из response_json
            actual_sorted = jmespath.search(f"pageable.sort.{key}", response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"pageable.sort." + key} - {expected_sorted} для сортировки - {sort}')
            logging.debug(
                    f'Актуальный параметр {"pageable.sort." + key} - {actual_sorted} для сортировки - {sort}')
            
            assert expected_sorted == actual_sorted, "Параметр empty неправильный."
        
        if key == 'unsorted':
            # # Если поле сортировки заполнялось, то истина, иначе - ложь
            expected_unsorted = True if sort is None else False
            
            # Получаем значение empty из response_json
            actual_unsorted = jmespath.search(f"pageable.sort.{key}", response_json)
            
            logging.debug(
                    f'Ожидаемый параметр {"pageable.sort." + key} - {expected_unsorted} для сортировки - {sort}')
            logging.debug(
                    f'Актуальный параметр {"pageable.sort." + key} - {actual_unsorted} для сортировки - {sort}')
            
            assert expected_unsorted == actual_unsorted, "Параметр empty неправильный."


# Проверка сохранения данных в БД (Можно попробовать доработать)))))
# Работает для шаблонной проверки без вложенности
def check_save_data_db(dbCursor, table, table_conditional, response_json, param_dictionary, count_object = 1):
    # Количество итераций всегда начинается с 0
    i = 0
    while i < count_object:
        for key in param_dictionary:
            if param_dictionary != param_ALL_additional_attribute_search:
                json_value = jmespath.search(f"{key}", response_json)
                json_value = reformatted_param(key, json_value)
                # Получаем значение записи в БД по условию
                db_query = params_record_db_condition(dbCursor, param_dictionary[key], table, table_conditional)
                
                # Логирование, для отладки
                logging.debug(f"№ строки - JSON-данные {json_value} - ключ {key}")
                logging.debug(f"№ строки - БД-данные {db_query} - ключ БД {param_dictionary[key]}")
                
                # Сверяем данные параметра json и ячейки БД
                assert db_query == json_value, f"Параметр в БД {param_dictionary[key]} = {db_query}.\n" \
                                               f"Значение в json {key} = {json_value}.\n"
        i += 1
    logging.info(f"JSON-данные тела ответа совпадает с данными в БД.")


# Функция рандомизации строки
def random_string(lenght):
    random_str = 'test_' + ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(lenght)])
    return random_str


# Вспомогательная функция для поиска строки в файле
def search_string_in_file(file_name, string_to_search):
    """Ищет данную строку в файле и возвращает строки, которые содержат данную, и номера этих строк"""
    line_number = 0
    list_of_results = []
    # Открытие файла в режиме "только для чтения". Использование with закроет файл после использования
    with open(file_name, 'r') as read_obj:
        # Чтение всех строк файла одна за другой
        for line in read_obj:
            # Для каждой строки файла проверка на содержание искомой строки
            line_number += 1
            if string_to_search in line:
                # Если да, номер строки и строка добавляются в список
                list_of_results.append((line_number, line.rstrip()))
    # Функция возвращает список строк, содержащих искомую, и их номеров в формате:
    # номер строки, строка
    return list_of_results


def search_index_in_file(file_name, string_to_search):
    """Ищет данную строку в файле и возвращает индекс строки, которая содержит данную"""
    line_number = 0
    list_of_results = []
    # Открытие файла в режиме "только для чтения". Использование with закроет файл после использования
    with open(file_name, 'r') as read_obj:
        # Чтение всех строк файла одна за другой
        for line in read_obj:
            # Для каждой строки файла проверка на содержание искомой строки
            line_number += 1
            if string_to_search in line:
                # Если да, номер строки добавляется в список
                list_of_results.append(line_number - 1)
    # Функция возвращает индекс строки, содержащую искомую
    return int(*list_of_results)


# Функция принимает на вход имя файла, индекс строки и строку, которую нужно записать
def rewrite_string(file_name, line_index, new_string):
    with open(file_name, 'r+') as f:
        lines = f.readlines()  # прочитать файл в список строк
        lines[line_index] = new_string  # записать в то же место измененную строку
        f.seek(0)  # указатель файла на начало
        f.writelines(lines)  # записать строки обратно в файл


# Функция подсчета количества страниц в методах получения списка
def pages_count(page_size, list_size):  # на вход подается размер страницы и размер списка записей из БД
    a = 0  # кол-во страниц изначально = 0
    if page_size >= list_size:  # если размер страницы больше количества записей в списке
        a = 1  # кол-во страниц = 1
    elif (list_size % page_size) == 0:  # если размер списка без остатка делится на размер страницы
        a = list_size // page_size  # кол-во страниц = размер списка/размер страницы (например, 35/7 = 5 страниц)
    elif (list_size % page_size) != 0:  # если размер списка делится на размер страницы с остатком
        a = (
                    list_size // page_size) + 1  # кол-во страниц = (размер списка / размер страницы) + 1 (например, 38/7 = 6 страниц)
    return a


def sort_by_alphabet(input_str):  # вспомогательная функция сортировки
    return input_str.lower()[0]  # строка.в_нижнем_регистре[первая ее буква]


# Функция проверки сортировки списка
def sort_list(sort_param, count, response_json):  # на вход подается параметр сортировки, кол-во элементов в списке,
    """ Пример sort_param: 'id:asc'. Распарсиваем строку на параметр сортировки и метод сортировки. """
    sort = sort_param[sort_param.find(':') + 1:]  # Получаем метод сортировки
    param = sort_param[:sort_param.find(':')]  # Получаем параметр сортировки, исключаем :
    
    #  Словарь параметров, в БД и в json параметры называются по разному
    dict_param = {'id': 'id', 'json_name': 'jsonName', 'name': 'name', 'identity': 'identities'}
    
    # откуда брать список (тут это тело ответа метода в формате JSON)
    i = 0  # переменная для итерации = 0
    list_sorted = []  # пустой список
    a_sort = None
    value = None
    while i < count:  # пока не дойдем до конца тела ответа
        value = jmespath.search(f"content[{i}].{dict_param[param]}",
                                response_json)  # получаем заданное значение из JSON тела ответа метода
        list_sorted.append(value)  # добавляем полученное значение в наш список
        i = i + 1  # двигаемся по циклу
    
    if type(value) == int:
        if sort == 'ASC' or sort == 'asc':
            a_sort = sorted(list_sorted)  # сортируем полученный список с помощью вспомогательной функции сортировки
        
        elif sort == 'DESC' or sort == 'desc':
            a_sort = sorted(list_sorted,
                            reverse = True)  # сортируем полученный список с помощью вспомогательной функции сортировки + в обратном порядке (reverse = True)
    if type(value) == str:
        if sort == 'asc' or sort == 'ASC':
            a_sort = sorted(list_sorted,
                            key = sort_by_alphabet)  # сортируем полученный список с помощью вспомогательной функции сортировки + в обратном порядке (reverse = True)
        
        elif sort == 'desc' or sort == 'DESC':
            a_sort = sorted(list_sorted,
                            key = sort_by_alphabet,
                            reverse = True)  # сортируем полученный список с помощью вспомогательной функции сортировки + в обратном порядке (reverse = True)
    if sort == 'json_name:ASC':
        a_sort = sorted(list_sorted,
                        key = sort_by_alphabet)  # сортируем полученный список с помощью вспомогательной функции сортировки + в обратном порядке (reverse = True)
    
    if type(value) is None:
        logging.debug('Параметр в json - value, не найден!')
    
    assert list_sorted == a_sort, 'Список не отсортирован'
    logging.debug(f'Список проверки сортировки по параметру {sort} - {list_sorted}')
    logging.debug(f'Проверка сортировка списка по параметру {sort} успешно')
    # return a_sort  # возвращаем отсортированный список


# Получение списка из тела ответа для сравнения с отсортированным списком
def get_list(param, count, source):  # на вход подается параметр сортировки, кол-во элементов в списке,
    # откуда брать список (тут это тело ответа метода в формате JSON)
    i = 0  # переменная для итерации = 0
    a = []  # пустой список
    while i < count:  # пока не дойдем до конца тела ответа
        value = jmespath.search(f"content[{i}].{param}",
                                source)  # получаем заданное значение из JSON тела ответа метода
        a.append(value)  # добавляем полученное значение в наш список
        i = i + 1  # двигаемся по циклу
    return a  # возвращаем список


# Получение количества записей на отображаемой странице списка
def r_count(count, size, page_count,
            offset):  # на вход подаются длина списка, размер страницы, количество страниц и смещение/номер страницы.
    a = 0  # Кол-во записей изначально = 0. если ни одно из условий не подойдет, то также вернется 0
    if offset == page_count - 1:  # Если номер страницы/смещение = последней странице
        if count % size != 0:  # и есть остаток от деления (например, 36 записей на 7 страницах)
            a = count % size  # то на странице отображается остаток от деления (на последней странице будет отображена 1 запись)
        else:  # иначе, если остатка нет (например, 35 записей на 5 страницах)
            a = count // size  # то на странице отображается размер списка / размер страницы записей (на последней странице будет отображаться 7 записей)
    elif offset < page_count - 1:  # если номер страницы/смещение != последней странице
        a = size  # то на странице должно отображаться количество, соответствующее размеру страницы
    return a  # возвращаем количество страниц


# or a function
def gen_datetime(min_year = 1900, max_year = datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days = 365 * years)
    return start + (end - start) * random.random()


# Функция генерации дополнительного атрибута
def gen_test_add_attribute_id(profile_api, dbCursor, i):
    """ Индексы функции
    0 :
    Добавление дополнительных атрибутов получателей МГП. Прямой сценарий.
    Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по name (Этот Name).
    Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по jsonName (Этот jsonName).
    1 : Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по name (Эти остальные параметры).
    2 : Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по jsonName (Эти остальные параметры).
    3 : Добавление дополнительных атрибутов получателей МГП. В теле не указан jsonName.
    4 :
    Обновление данных дополнительного атрибута. Прямой сценарий (Это создаем).
    Удалить дополнительный атрибут. Прямой сценарий.
    Удалить дополнительный атрибут. Использовать jsonName в качестве идентификатора.
    5 :
    Получение информации о дополнительном атрибуте. Прямой сценарий.
    Получение информации о дополнительном атрибуте. Использовать jsonName в качестве идентификатора.
    Получение списка дополнительных атрибутов(GET). Прямой сценарий (полное совпадение).
    Получение списка дополнительных атрибутов(POST). Прямой сценарий (полное совпадение).
    Обновление данных дополнительного атрибута. Прямой сценарий (На это обновляем).
    Обновление данных дополнительного атрибута. Указаны данные со старой информацией.
    Получение списка дополнительных атрибутов (GET). Указан только names.
    Получение списка дополнительных атрибутов (GET). Указан только jsonNames.
    Получение списка дополнительных атрибутов (GET). Некорректный names.
    Получение списка дополнительных атрибутов (GET). Некорректный jsonNames.
    Получение списка дополнительных атрибутов. Частичное совпадение.
    Удалить список атрибутов из группы. Несуществующий name.
    6 :
    Добавить атрибуты в группу. Прямой сценарий - Добавление 1 атрибута.
    Добавить атрибуты в группу. Несуществующий name.
    Обновление данных дополнительного атрибута. Использовать jsonName в качестве идентификатора ("Это создаем").
    7 :
    Получить список атрибутов входящих в группу. Прямой сценарий.
    Удалить список атрибутов из группы. Прямой сценарий.
    8 :
    Обновление данных дополнительного атрибута. Использовать jsonName в качестве идентификатора (На это обновляем).
    9 :
    Обновление данных дополнительного атрибута. Некорректный id.
    10 :
    Обновление данных дополнительного атрибута. Указаны не все поля в теле запроса.
    Добавить атрибуты в группу. Такие данные уже есть в системе.
    11 : Добавить атрибуты в группу. Добавление нескольких атрибутов.
    """
    logging.debug('Запуск функции gen_test_add_attribute_id')
    try:
        # Получаем параметр в БД условию
        additional_attribute_id_new = params_record_db_condition(dbCursor, "id", "additional_attribute",
                                                                 f"json_name = '{additional_attribute_jsonName_new[i]}'")
    
    except TypeError:
        body = {
            "display": additional_attribute_display_new[i],
            "required": additional_attribute_required_new[i],
            "name": f"{additional_attribute_name_new[i]}",
            "jsonName": f"{additional_attribute_jsonName_new[i]}",
            "fieldOrder": additional_attribute_fieldOrder_new[i],
            "fieldType": additional_attribute_fieldType_new[i],
            "userType": f"{additional_attribute_userType_new[i]}",
            "creationDate": f"{additional_attribute_creationDate_new[i]}",
            "region": f"{additional_attribute_region_new[i]}",
            "metadata": additional_attribute_metadata_new[i]
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        profile_api.post("/profile/attributes/additional", headers = headers,
                         data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Получаем параметр в БД условию
        additional_attribute_id_new = params_record_db_condition(dbCursor, "id", "additional_attribute",
                                                                 f"json_name = '{additional_attribute_jsonName_new[i]}'")
    
    logging.debug('Завершение функции gen_test_add_attribute_id')
    
    return additional_attribute_jsonName_new[i], additional_attribute_id_new


# Функция генерации employee ID для удаления
# 0 - Удаление сотрудника. Прямой сценарий
# 1 - Удаление сотрудника. Удаление навсегда (permanent - true)
# 2 - Удаление сотрудника. Не указывать permanent
# 3 -
def gen_test_delete_employee_id(profile_api, i):
    logging.debug(f"Запуск функции gen_test_delete_employee_id")  # Логируем тело ответа
    
    body = {
        "attributes": {
            "first_name": f"{employee_management_delete_first_name[i]}",
            "last_name": f"{employee_management_delete_last_name[i]}",
            "patronymic": f"{employee_management_delete_patronymic[i]}",
            "inn": f"{employee_management_delete_inn[i]}",
            "organization_head": employee_management_delete_org_head[i],
            "registration_address": f"{employee_management_delete_registration_address[i]}",
            "residential_address": f"{employee_management_delete_residential_address[i]}",
            "representative": employee_management_delete_representative[i],
            "phone": f"{employee_management_delete_phone[i]}",
            "email": f"{employee_management_delete_email[i]}",
            "notification_email": f"{employee_management_delete_email[i]}",
            "identity_document_link": f"{employee_management_delete_identity_document_link[i]}",
            "snils": f"{employee_management_delete_snils[i]}",
            "document_type": f"{employee_management_delete_document_type[i]}",
            "document_number": f"{employee_management_delete_doc_number[i]}",
            "document_issuer": f"{employee_management_delete_document_issuer[i]}",
            "subdivision_code": f"{employee_management_delete_subdivision_code[i]}",
            "document_date": f'{employee_management_delete_document_date[i]}'
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "orgId": f"{employee_management_org_id}"
    }
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Отправляем запрос
    response = profile_api.post(
            "/employee-management/employee/add", params = params, headers = headers,
            data = body_json)  # Записываем ответ метода POST в переменную response
    
    # Парсинг тела ответа
    response_json = parse_response_json(response)[0]
    
    employee_management_add_id_new_2 = jmespath.search("id", response_json)
    
    logging.debug(f"Завершение функции gen_test_delete_employee_id")  # Логируем тело ответа
    return employee_management_add_id_new_2


# Функция генерации employee ID
# Индексы тестовых данных
# 0 :
# Получение списка сотрудников (в том числе помеченных как удаленные). Прямой сценарий
# 1 :
# Получение списка сотрудников (в том числе помеченных как удаленные). Выбрано отображение только указанных атрибутов
# Получение информации о сотруднике по его идентификатору. Прямой сценарий
# Получение информации о сотруднике по его идентификатору. Указан видимый атрибут
# Получение информации о сотруднике по его идентификатору. Не указаны параметры запроса
# 2 :
# Изменение атрибутов сотрудника. Не указывать тело запроса
# 3 :
# Добавление сотрудника. Прямой сценарий
# Добавление сотрудника. Несуществующий orgID
def gen_test_employee_id(profile_api, dbCursor, i):
    logging.debug(f"Запуск функции - gen_test_employee_id")
    
    body = {
        "attributes": {
            "first_name": f"{employee_management_add_first_name[i]}",
            "last_name": f"{employee_management_add_last_name[i]}",
            "patronymic": f"{employee_management_add_patronymic[i]}",
            "inn": f"{employee_management_add_inn[i]}",
            "organization_head": employee_management_add_org_head[i],
            "registration_address": f"{employee_management_add_registration_address[i]}",
            "residential_address": f"{employee_management_add_residential_address[i]}",
            "representative": employee_management_add_representative[i],
            "phone": f"{employee_management_add_phone[i]}",
            "email": f"{employee_management_add_email[i]}",
            "notification_email": f"{employee_management_add_notification_email[i]}",
            "identity_document_link": f"{employee_management_add_identity_document_link[i]}",
            "snils": f"{employee_management_add_snils[i]}",
            "document_type": f"{employee_management_add_document_type[i]}",
            "document_number": f"{employee_management_add_doc_number[i]}",
            "document_issuer": f"{employee_management_add_document_issuer[i]}",
            "subdivision_code": f"{employee_management_add_subdivision_code[i]}",
            "documents_folder": f"{employee_management_add_document_folder[i]}",
            "document_date": f'{employee_management_add_document_date[i]}',
            "term_of_office": f"{employee_management_add_term_of_office[i]}",
            "dismissal_date": f"{employee_management_add_dismissal_date[i]}",
            "employment_date": f"{employee_management_add_employment_date[i]}",
            "work_length": f"{employee_management_add_work_length[i]}",
            "salary": f"{employee_management_add_salary[i]}",
            "position": f"{employee_management_add_position[i]}",
            "citizenship": f"{employee_management_add_citizenship[i]}"
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "orgId": f"{employee_management_org_id}"
    }
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Отправляем запрос
    response = profile_api.post(
            "/employee-management/employee/add", params = params, headers = headers,
            data = body_json)  # Записываем ответ метода POST в переменную response
    
    # Парсинг тела ответа
    parse_response_json(response)
    
    # Получаем параметр в БД условию
    employee_management_add_id_new_2 = params_record_db_condition(dbCursor, "*",
                                                                  "emp_employee JOIN  public.emp_employee_attribute ON public.emp_employee.id=public.emp_employee_attribute.employee_id",
                                                                  f"attribute_id = 'inn' and value = '{employee_management_add_inn[i]}'")
    
    logging.debug(f"Завершение функции - gen_test_employee_id")
    return employee_management_add_id_new_2, body


# Индексы переменной i
# 0 :
# Изменение атрибутов сотрудника. Прямой сценарий (Создание)
# 1 :
# Изменение атрибутов сотрудника. Прямой сценарий (Обновление)
# Функция генерации employee ID для обновления сотрудника
def gen_test_update_employee_id(profile_api, i):
    logging.debug(f"Запуск функции - gen_test_update_employee_id")  # Логируем
    
    body = {
        "attributes": {
            "first_name": f"{employee_management_update_first_name[i]}",
            "last_name": f"{employee_management_update_last_name[i]}",
            "patronymic": f"{employee_management_update_patronymic[i]}",
            "inn": f"{employee_management_update_inn[i]}",
            "organization_head": employee_management_update_org_head[i],
            "registration_address": f"{employee_management_update_registration_address[i]}",
            "residential_address": f"{employee_management_update_residential_address[i]}",
            "representative": employee_management_update_representative[i],
            "phone": f"{employee_management_update_phone[i]}",
            "email": f"{employee_management_update_email[i]}",
            "notification_email": f"{employee_management_update_notification_email[i]}",
            "identity_document_link": f"{employee_management_update_identity_document_link[i]}",
            "snils": f"{employee_management_update_snils[i]}",
            "document_type": f"{employee_management_update_document_type[i]}",
            "document_number": f"{employee_management_update_doc_number[i]}",
            "document_issuer": f"{employee_management_update_document_issuer[i]}",
            "subdivision_code": f"{employee_management_update_subdivision_code[i]}",
            "documents_folder": f"{employee_management_update_document_folder[i]}",
            "document_date": f'{employee_management_update_document_date[i]}',
            "term_of_office": f"{employee_management_update_term_of_office[i]}",
            "dismissal_date": f"{employee_management_update_dismissal_date[i]}",
            "employment_date": f"{employee_management_update_employment_date[i]}",
            "work_length": f"{employee_management_update_work_length[i]}",
            "salary": f"{employee_management_update_salary[i]}",
            "position": f"{employee_management_update_position[i]}",
            "citizenship": f"{employee_management_update_citizenship[i]}"
        },
    }
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "orgId": f"{employee_management_org_id}"
    }
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Отправляем запрос
    response = profile_api.post(
            "/employee-management/employee/add", params = params, headers = headers,
            data = body_json)  # Записываем ответ метода POST в переменную response
    
    # Парсинг тела ответа
    response_json = parse_response_json(response)[0]
    
    # Достаем employee_id из тела ответа
    employee_management_add_id_new_2 = jmespath.search('id',
                                                       response_json)  # Ищем каждый параметр из файла с параметрами json
    logging.debug(f"Завершение функции - gen_test_update_employee_id")  # Логируем
    return employee_management_add_id_new_2, body


# Функция генерации base attribute ID
"""Использование индексов i
0 :
Для функции поиска base attribute ID.
Добавление данных для пользователя по атрибутам. Прямой сценарий.
1 :
Для функции генерации ревизий атрибута.
Обновление данных пользователя, сотрудником РОУ АПК. Прямой сценарий.
2 :
Для функции поиска base attribute.
Добавить базовый атрибут. Базовый атрибут уже существует по jsonName (Данные не создаются, но используются для проверки того, что они не добавятся)
Получение списка базовых атрибутов (GET). Прямой сценарий (полное совпадение).
Получение списка базовых атрибутов (GET). Указан только names.
Получение списка базовых атрибутов (GET). Указан только identities.
Получение списка базовых атрибутов (GET). Некорректный names.
Получение списка базовых атрибутов (GET). Частичное совпадение.
Получение списка базовых атрибутов (GET). Некорректный identities.
Получение списка базовых атрибутов (POST). Прямой сценарий.
Получение списка базовых атрибутов (POST). Несуществующий names.
Получение списка базовых атрибутов (POST). Частичное совпадение.
Получение списка базовых атрибутов (POST). Несуществующий identities.
Получение информации о базовом атрибуте. Прямой сценарий.
Получение информации о базовом атрибуте. Использовать jsonName в качестве идентификатора.
3 :
Изменить базовый атрибут. Прямой сценарий (Создаем).
4 :
Изменить базовый атрибут. Прямой сценарий (Изменяем).
Удалить базовый атрибут. Прямой сценарий.
Удалить базовый атрибут. Использовать jsonName в качестве идентификатора.
5 :
Добавить базовый атрибут. Прямой сценарий.
Добавить базовый атрибут. Базовый атрибут уже существует по jsonName.
6 :
Добавить базовый атрибут. Неверный формат поля creationData по количеству символов.
7 :
Изменить базовый атрибут. Некорректный id.
8 :
Изменить базовый атрибут. Не указано тело запроса.
"""


def gen_test_base_attribute_id(profile_api, dbCursor, i):
    logging.debug('Запуск функции gen_test_base_attribute_id')
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
    profile_api.post("profile/attributes/base", headers = headers,
                     data = body_json)  # Записываем ответ метода GET в переменную response
    
    # Получаем параметр в БД условию
    base_attribute_id_new_2 = params_record_db_condition(dbCursor, "id", "base_attribute",
                                                         f"name = '{base_attribute_name_new[i]}' and json_name = '{base_attribute_json_name_new[i]}'")
    
    logging.debug('Завершение функции gen_test_base_attribute_id')
    return base_attribute_id_new_2


# Номера итерации генерации тестовых данных в списке
# 0 :
# Создание пользователя в сервисе Профиль. Прямой сценарий
# 1 :
# Редактирование получателя МГП (PUT /profile/mgp-recipient/{id}). Некорректные данные поля status
# Редактирование получателя МГП (PUT /profile/mgp-recipient/{id}). Указаны данные со старой информацией
# Редактирование получателя МГП (PUT /profile/mgp-recipient/{id}). Пустое тело запроса
# Редактирование получателя МГП (PUT /profile/mgp-recipient/{id}). Не указано тело запроса
# Получение получателя МГП по идентификатору. Прямой сценарий
# Получение идентификатора пользователя по идентификатору получателя МГП. Прямой сценарий
# Получение получателя МГП по идентификатору пользователя. Прямой сценарий
# 2 :
# Для функции поиска user ID -  find_test_user_id
# Для функции поиска существующего user ID со списком изменений атрибутов - find_test_revision_user_id
# Для функции генерации ревизий атрибута - gen_attr_revisions
# Редактирование получателя МГП (PUT /profile/mgp-recipient/{id}). Переход со статуса POTENTIAL в статус ARCHIVE
# 3 :
# Для функции смены статуса получателя МГП у user ID - change_test_status_mgp
# Для функции поиска user ID - 2 find_test_user_id_2
# Редактирование получателя МГП (PUT /profile/mgp-recipient/{id}). Переход со статуса POTENTIAL в статус ACTIVE
# 4:
# Конструктор для получения данных о всех пользователях по конкретным атрибутам. Прямой сценарий
# 5 Для функции генерации сист. атрибутов у пользователя
# Функция генерации user ID
def gen_test_user_id(profile_api, dbCursor, i):
    logging.debug(f"Запуск функции gen_test_user_id")  # Логируем тело ответа
    
    params = {
        "id": f"{profile_user_id_new[i]}",
        "region": f"{profile_user_region_new[i]}",
        "role": f"{profile_user_role_new[i]}"
    }
    # Отправляем запрос
    profile_api.post(
            "profile/user", params = params)  # Записываем ответ метода POST в переменную response
    
    # Получаем параметр в БД условию
    user_uuid_0_new = params_record_db_condition(dbCursor, "id", "mgp_recipient",
                                                 f"user_id = '{profile_user_id_new[i]}'")
    
    logging.debug(f"Получили из gen_test_user_id {profile_user_id_new[i]} и {user_uuid_0_new}")  # Логируем тело ответа
    
    logging.debug(f"Завершение функции gen_test_user_id")  # Логируем тело ответа
    
    return profile_user_id_new[i], user_uuid_0_new


# Функция смены статуса получателя МГП у user ID
# Для метода (PUT /profile/mgp-recipient/{id}) Редактирование получателя МГП
def change_test_status_mgp(new_status, profile_api, dbCursor):
    logging.debug(f"Запуск функции change_test_status_mgp")  # Логируем тело ответа
    
    # Номер итерации для генерации данных
    i = 3
    
    # Вызов функции генерации user ID
    profile_user_id, user_uuid_0_new = gen_test_user_id(profile_api, dbCursor, i)
    
    body = {
        "status": f"{new_status}",
        "statusDate": f"{profile_mgp_recipient_id_status_date_new}",
        "okopf": f"{profile_mgp_recipient_id_okopf_new}",
        "userId": f"{profile_user_id}"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Отправляем запрос
    profile_api.put(
            f"/profile/mgp-recipient/{user_uuid_0_new}", headers = headers,
            data = body_json)  # Записываем ответ метода POST в переменную response
    
    logging.debug(f"Завершение функции change_test_status_mgp")  # Логируем тело ответа
    return profile_user_id, user_uuid_0_new


# Функция поиска user ID
def find_test_user_id(profile_api, dbCursor):
    logging.debug(f"Запуск функции find_test_user_id")  # Логируем тело ответа
    user_id_new = None
    try:
        # Получаем параметр в БД условию
        user_id_new = params_record_db_condition(dbCursor, "shtp_user_id", "shtp_user",
                                                 f"shtp_user_id like '%test%'")
    except TypeError:
        if user_id_new is None:
            #  Номер итерации для генерации данных
            i = 2
            
            # Вызов функции генерации user ID
            user_id_new = gen_test_user_id(profile_api, dbCursor, i)[0]
    
    # Отправляем запрос
    response = profile_api.get(f"/profile/user/{user_id_new}")  # Записываем ответ метода GET в переменную response
    
    # Парсинг тела ответа
    parse_response_json(response)
    
    logging.debug(f"user ID - {user_id_new}")  # Логируем тело ответа
    
    # Получаем параметр в БД условию
    user_uuid_1_new = params_record_db_condition(dbCursor, "id", "mgp_recipient",
                                                 f"user_id = '{user_id_new}'")
    
    logging.debug(f"Завершение функции find_test_user_id")  # Логируем тело ответа
    return user_id_new, user_uuid_1_new


# Функция поиска user ID - 2
# Для метода POST/profile/mgp-recipient-ids Получение получателей МГП по идентификаторам пользователя (ЮЛ/ФЛ/ИП)
def find_test_user_id_2(user_id_old, profile_api, dbCursor):
    logging.debug(f"Запуск функции find_test_user_id_2")  # Логируем тело ответа
    user_id_2_new = None
    try:
        # Получаем параметр в БД условию
        user_id_2_new = params_record_db_condition(dbCursor, "shtp_user_id", "shtp_user",
                                                   f"shtp_user_id != '{user_id_old}' and shtp_user_id like '%test%'")
    
    except TypeError:
        if user_id_2_new is None:
            #  Номер итерации для генерации данных
            i = 3
            
            # Вызов функции генерации user ID
            user_id_2_new = gen_test_user_id(profile_api, dbCursor, i)[0]
    
    # Отправляем запрос
    response = profile_api.get(f"/profile/user/{user_id_2_new}")  # Записываем ответ метода GET в переменную response
    
    # Парсинг тела ответа
    parse_response_json(response)
    
    logging.debug(f"user ID 2 - {user_id_2_new}")  # Логируем тело ответа
    logging.debug(f"Завершение функции find_test_user_id_2")  # Логируем тело ответа
    
    return user_id_2_new


# Функция поиска заполненного атрибута для пользователя
def find_test_attribute_data_constructor(profile_api, dbCursor, user_id_data_constructor_new = None):
    logging.debug(f"Запуск функции find_test_attribute_data_constructor")  # Логируем тело ответа
    
    #  Если при вызове функции не указали явно user_id, то ищем тестового пользователя
    if user_id_data_constructor_new is None:
        # Получаем параметр в БД условию
        user_id_data_constructor_new = params_record_db_condition(dbCursor, "shtp_user_id", "shtp_user",
                                                                  "shtp_user_id like '%test%'")
    
    # Ищем заполненный атрибут, у пользователя user_id_data_constructor_new
    try:
        name_full_attribute_new = params_record_db_condition(dbCursor, "name", "user_attribute",
                                                             f"user_id = '{user_id_data_constructor_new}'")
    
    # Если заполненного атрибута нет, то генерируем его у пользователя user_id_data_constructor_new
    except TypeError:
        name_full_attribute_new = gen_attr_revisions(profile_api, dbCursor, user_id_data_constructor_new)
    
    # Получаем значение атрибута в БД условию
    value_full_attribute_new = params_record_db_condition(dbCursor, "value", "user_attribute",
                                                          f"user_id = '{user_id_data_constructor_new}' and name = '{name_full_attribute_new}'")
    
    params = {
        'attributes': f'{name_full_attribute_new}'
    }
    
    # Отправляем запрос
    response = profile_api.get(
            f"profile/{user_id_data_constructor_new}/data-constructor",
            params = params)  # Записываем ответ метода POST в переменную response
    
    # Парсинг тела ответа
    parse_response_json(response)
    
    logging.debug(f"user ID - {user_id_data_constructor_new}")  # Логируем тело ответа
    logging.debug(f"attribute - {name_full_attribute_new}")  # Логируем тело ответа
    logging.debug(f"Завершение функции find_test_attribute_data_constructor")  # Логируем тело ответа
    return name_full_attribute_new, value_full_attribute_new, user_id_data_constructor_new


# Функция поиска пользователя, его региона и типа, с заполненным атрибутом
def find_test_user_id_data_constructor(profile_api, dbCursor, i):
    """
    Описание использования всех i индексов
    0 :
    Получение данных о пользователе по типу атрибутов. Прямой сценарий
    Добавление данных для пользователя по атрибутам. Прямой сценарий
    Конструктор для получения данных о всех пользователях по конкретным атрибутам. Прямой сценарий (Пользователь СХТП)
    1 :
    Получение данных о пользователе по типу атрибутов. 1. Тип атрибутов - ADDITIONAL, 2. Несуществующий type 3.
    Конструктор для получения данных о всех пользователях по конкретным атрибутам. Не указаны параметры запроса
    Конструктор для получения данных о всех пользователях по конкретным атрибутам. Указан только attributes
    Поиск пользователей по атрибутам (GET). Прямой сценарий
    2 :
    Получение всех данных о пользователе. Прямой сценарий
    Получение всех данных о пользователе. Указан только userId
    3 :
    Конструктор для получения данных о пользователе. Прямой сценарий
    Получение информации о пользователе. Прямой сценарий
    4 :
    Конструктор для получения данных о всех пользователях по конкретным атрибутам. Прямой сценарий
    Редактирование пользователя в сервисе Профиль. Прямой сценарий (Создание)
    Поиск пользователей по атрибутам (POST). Прямой сценарий
    Поиск пользователей по атрибутам (POST). Несуществующий attributes
    Поиск пользователей по атрибутам (POST). Не указан attributes
    Поиск пользователей по атрибутам (POST). Не указан regionId
    Поиск пользователей по атрибутам (POST). Несуществующий regionId
    Добавление данных для пользователя по атрибутам. Не указано тело запроса
    5:
    Функция установки статуса для поиска пользователя по статусу
    6:
    Редактирование пользователя в сервисе Профиль. Прямой сценарий (Обновление)
    """
    logging.debug(f"Вызов функции: find_test_user_id_data_constructor")  # Логируем тело ответа
    
    # Тут пробуем получить user_id, если он не занят и существует
    try:
        # Получаем параметр в БД условию (Слишком сложный запрос можно и оставить обычный способ, спорно)
        user_id = params_record_db_condition(dbCursor,
                                             # SELECT
                                             "shtp_user_id",
                                             # FROM
                                             "(SELECT ROW_NUMBER () OVER (ORDER BY shtp_user_id), shtp_user_id FROM shtp_user join user_attribute "
                                             f"ON shtp_user.shtp_user_id=user_attribute.user_id "
                                             f"WHERE shtp_user_id like '%test%')x",
                                             # WHERE
                                             f"ROW_NUMBER = {i + 1}")
        
        logging.debug(f"Строка в БД {i} - пользователь - {user_id}")  # Логируем тело ответа
    # Если user_id отсутствует в БД, то генерируем новый с тем же индексом i
    except TypeError:
        # Todo, в целом думаю индексы подойдут и к gen_test_user_id функции, но это стоит проверить
        user_id = gen_test_user_id(profile_api, dbCursor, i)[0]
    
    # Вызываем функцию поиска заполненного атрибута для пользователя
    name_full_attribute = find_test_attribute_data_constructor(profile_api, dbCursor, user_id)[0]
    
    logging.debug(f"user ID - {user_id}")  # Логируем тело ответа
    logging.debug(f"attribute - {name_full_attribute}")  # Логируем тело ответа
    
    # Отправляем запрос
    response = profile_api.get(
            f"profile/user/{user_id}")  # Записываем ответ метода POST в переменную response
    
    # Парсинг тела ответа
    response_json = parse_response_json(response)[0]
    
    logging.debug(f"user ID - {user_id}")
    
    region = jmespath.search(f"region", response_json)
    logging.debug(f"region - {region}")
    
    user_type = jmespath.search(f"role", response_json)
    logging.debug(f"role - {user_type}")
    
    logging.debug(f"Завершение функции: find_test_user_id_data_constructor")  # Логируем тело ответа
    
    return user_id, region, user_type


# Функция поиска существующего user ID со списком изменений атрибутов, НЕ ИЗМЕНЯТЬ!
def find_test_revision_user_id(profile_api, dbCursor):
    logging.debug('Запуск функции - find_test_revision_user_id')
    # Объявление переменной, для того что бы блок except не ругался что переменной нет
    user_id_new = None
    revision_id = None
    att_name = None
    # Проверяем наличие в БД по name
    try:
        # Получаем значение user_id в БД без условий
        user_id_new = params_record_db_without_condition(dbCursor, "user_id", "user_attribute_aud")
        
        # Получаем значение name в БД без условий
        att_name = params_record_db_without_condition(dbCursor, "name", "user_attribute_aud")
        
        # Получаем значение rev в БД без условий
        revision_id = params_record_db_without_condition(dbCursor, "rev", "user_attribute_aud")
    
    except TypeError:
        #  Если не нашли ни одного user_id, то генерируем новый
        if user_id_new is None:
            i = 2
            user_id_new = gen_test_user_id(profile_api, dbCursor, i)[0]
    
    params = {
        "userId": f'{user_id_new}'
    }
    
    # Отправляем запрос
    response = profile_api.get(f"/profile/user/{user_id_new}",
                               params = params)  # Записываем ответ метода GET в переменную response
    # Парсинг тела ответа
    parse_response_json(response)
    
    logging.debug(f"user ID - {user_id_new}")  # Логируем тело ответа
    logging.debug('Завершение функции - find_test_revision_user_id')
    
    return user_id_new, att_name, revision_id


# Функция генерации ревизий атрибута
def gen_attr_revisions(profile_api, dbCursor, user_id):
    logging.debug(f"Запуск функции gen_attr_revisions")  # Логируем тело ответа
    
    # Номер итерации для генерации нового пользователя
    i = 2
    
    # Тут исключаем пользователя в БД, который ошибочно записан как ''
    if user_id == '':
        # Генерируем нового пользователя
        user_id = gen_test_user_id(profile_api, dbCursor, i)
    
    # Номер итерации для генерации base attribute ID
    j = 1
    
    # Вызов функции генерации base attribute ID
    gen_test_base_attribute_id(profile_api, dbCursor, j)
    
    body = {
        f"{base_attribute_json_name_new[j]}": f"{full_attribute_value_new}",
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Заполняем атрибут у пользователя.
    # Отправляем запрос.
    profile_api.put(f"profile/{user_id}/data", headers = headers,
                    data = body_json)  # Записываем ответ метода POST в переменную response
    
    logging.debug(f"Завершение функции gen_attr_revisions")  # Логируем тело ответа
    return base_attribute_json_name_new[j]


# Todo дописать функцию, не работает до конца
# Функция генерации ревизий удаленного атрибута
def gen_del_attr_revisions(profile_api, dbCursor):
    logging.debug("Запуск функции gen_del_attr_revisions")
    i = 2
    gen_test_user_id(profile_api, dbCursor, i)
    
    try:
        # Получаем параметр в БД условию
        base_attr_deleted = params_record_db_condition(dbCursor, "json_name", "base_attribute",
                                                       f"deleted = true and json_name like '%test%'")
        print(base_attr_deleted)
    except TypeError:
        # Получаем параметр в БД условию
        base_attr_deleted = params_record_db_condition(dbCursor, "json_name", "base_attribute",
                                                       f"json_name like '%test%'")
        print(base_attr_deleted)
    
    i = 1
    gen_test_base_attribute_id(profile_api, dbCursor, i)
    
    body = {
        f"{base_attribute_json_name_new}": "432",
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Сначала заполним атрибут у пользователя.
    # Отправляем запрос.
    profile_api.put(
            f"profile/{profile_user_id_new}/data", headers = headers,
            data = body_json)  # Записываем ответ метода POST в переменную response
    
    params = {
        f"attributes": f"{base_attribute_json_name_new}",
    }
    
    # Посмотрим что атрибут заполнился у пользователя.
    # Отправляем запрос.
    profile_api.get(
            f"profile/{profile_user_id_new}/data-constructor",
            params = params)  # Записываем ответ метода POST в переменную response
    
    # Теперь удалим атрибут
    
    # params = {
    #     f"useJsonNameAsId": True,
    # }
    
    # Отправляем запрос
    # response = profile_api.delete(
    #    f"profile/attributes/base/{base_attribute_json_name_new}", params=params)  # Записываем ответ метода POST в переменную response
    
    # # Проверяем наличие в БД по name
    # query_count = f"SELECT id FROM shtp_user WHERE shtp_user_id = '{profile_user_id_new}'"
    # dbCursor.execute(query_count)
    # user_id_new_2 = dbCursor.fetchone()[0]
    logging.debug("Завершение функции gen_del_attr_revisions")
    
    return params


# Функция создания группы, для ее последующего удаления
def gen_del_group(profile_api, i):
    # Индексы функции
    # 0 - Удалить группу. Прямой сценарий
    # 1 - Удалить список атрибутов из группы. Прямой сценарий
    # 2 - Удалить список атрибутов из группы. Не указывать тело запроса
    # 3 - Удалить список атрибутов из группы. Атрибута нет в группе
    logging.debug(f'Запуск функции gen_del_group')
    body = {
        "name": f"{group_gen_del_name[i]}",
        "description": f"{group_gen_del_description}",
        "role": f"{group_gen_role[i]}"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Отправляем запрос
    profile_api.post("group", headers = headers, data = body_json)  # Записываем ответ метода POST в переменную response
    
    # Отправляем запрос
    response = profile_api.get(f"/group/{group_gen_del_name[i]}")  # Записываем ответ метода GET в переменную response
    
    # Парсинг тела ответа
    parse_response_json(response)
    
    logging.debug(f'Завершение функции gen_del_group')
    return group_gen_del_name[i]


# Функция добавления атрибутов в группу, для их удаления из группы
def gen_add_attr_del_group(profile_api, dbCursor, name):
    # name [1] - используется для тестов:
    # Удалить список атрибутов из группы. Прямой сценарий.
    # Получить список атрибутов входящих в группу. Прямой сценарий.
    logging.debug(f'Запуск функции gen_add_attr_del_group')
    
    # Номер итерации для генерации данных
    j = 7
    # Вызов функции для генерации доп. атрибута
    group_gen_del_attr_name = gen_test_add_attribute_id(profile_api, dbCursor, j)[0]
    
    body = {
        'attributes': [
            {
                "attrName": f"{group_gen_del_attr_name}",
                "block": f"{group_gen_del_block}"
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    profile_api.post(f'/group/{name}/attributes', headers = headers, data = body_json)
    
    logging.debug(f'Завершение функции gen_add_attr_del_group')
    
    return group_gen_del_attr_name


# Функция создания группы
def gen_group(profile_api, i):
    """
    Индексы функции.
    0
    Обновить группу. Прямой сценарий (Создать).
    Получить данные о группе. Прямой сценарий.
    Добавить атрибуты в группу. Несуществующий attrName.
    Добавить атрибуты в группу. Такие данные уже есть в системе.
    Получить список атрибутов входящих в группу. Прямой сценарий.
    Добавить атрибуты в группу. Прямой сценарий - Добавление 1 атрибута (Создание группы).
    1
    Получить список атрибутов входящих в группу. Прямой сценарий.
    2
    Создать группу. Прямой сценарий.
    3
    Обновить группу. Прямой сценарий (Обновить).
    4
    Добавить атрибуты в группу. Добавление нескольких атрибутов.
    5
    Добавить атрибуты в группу. Указаны не все поля в теле запроса.
    6
    Обновить группу. Некорректные данные поля role.
    """
    logging.debug('Запуск функции gen_group')
    body = {
        "name": f"{group_gen_name[i]}",
        "description": f"{group_gen_description}",
        "role": f"{group_gen_role[i]}"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Отправляем запрос
    profile_api.post("group", headers = headers, data = body_json)  # Записываем ответ метода POST в переменную response
    
    # Отправляем запрос
    response = profile_api.get(
            f"/group/{group_gen_name[i]}")  # Записываем ответ метода GET в переменную response
    
    # Парсинг тела ответа
    parse_response_json(response)
    
    logging.debug('Завершение функции gen_group')
    
    return group_gen_name[i]


# Функция генерации системного атрибута
def gen_system_attributes(profile_api, i):
    """
    Индексы функции
    0 :
    Получение системного атрибута по его json name. Прямой сценарий
    Изменение системного атрибута. Прямой сценарий (Создание)
    1 :
    Изменение системного атрибута. Прямой сценарий (Обновление)
    Изменение системного атрибута. Пустое тело запроса
    Изменение системного атрибута. Использовать jsonName в качестве идентификатора (Создание)
    Изменение системного атрибута. Не указано тело запроса
    Изменение системного атрибута. Некорректные данные поля userType (Создание)
    Получение системного атрибута по идентификатору. Прямой сценарий
    Получение существующих системных атрибутов. Прямой сценарий
    Получение существующих системных атрибутов. Указан только jsonNames
    Получение существующих системных атрибутов. Указан только jsonNames
    Получение существующих системных атрибутов. Некорректный jsonNames
    Получение существующих системных атрибутов. Некорректный names
    Удаление системного атрибута. Прямой сценарий
    2 :
    Получение значений системных атрибутов для указанного пользователя. Прямой сценарий
    Изменение системного атрибута. Использовать jsonName в качестве идентификатора (Обновление)
    Обновление значений системных атрибутов для указанного пользователя. Регион пользователя и system_attributes разные
    3 :
    Добавление системного атрибута. Прямой сценарий
    4 :
    Добавить атрибуты в группу. Добавление нескольких атрибутов
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений
    5 :
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений
    Изменение системного атрибута. Некорректный id
    Изменение системного атрибута. Несуществующий id
    6 :
    Добавление системного атрибута. Некорректные данные поля userType
    Добавление системного атрибута. Некорректные данные поля region
    Изменение системного атрибута. Некорректные данные поля userType (Обновление)
    Обновление значений системных атрибутов для указанного пользователя. Тип пользователя и system_attributes разные
    """
    logging.debug("Запуск функции gen_system_attributes")
    
    body = {
        "display": system_attributes_display_new[i],
        "required": system_attributes_required_new[i],
        "name": f"{system_attributes_name_new[i]}",
        "jsonName": f"{system_attributes_jsonName_new[i]}",
        "fieldOrder": system_attributes_fieldOrder_new[i],
        "fieldType": system_attributes_fieldType_new[i],
        "userType": f"{system_attributes_userType_new[i]}",
        "region": f"{system_attributes_region_new[i]}",
        "metadata": system_attributes_metadata_new[i]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Отправляем запрос
    profile_api.post("/profile/system-attributes/add", headers = headers,
                     data = body_json)  # Записываем ответ метода GET в переменную response
    
    logging.debug("Завершение функции gen_system_attributes")
    
    return system_attributes_jsonName_new[i], system_attributes_name_new[i]


# Функция генерации user ID для проверки системных атрибутов
def gen_test_user_id_system_attr(profile_api, dbCursor, i):
    """# Индекс функции
    2 :
    Для функции генерации системных атрибутов у пользователя (Получение значений системных атрибутов для указанного пользователя. Прямой сценарий)
    3 :
    Для функции генерации системных атрибутов у пользователя (Обновление значений системных атрибутов для указанного пользователя. Прямой сценарий (Создание))
    4 :
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений
    6 :
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений, один из них не подходящий
    7 :
    Обновление значений системных атрибутов для указанного пользователя. Пустое тело запроса
    """
    logging.debug(f"Запуск функции gen_test_user_id_system_attr")  # Логируем тело ответа
    
    params = {
        "id": f"{system_attributes_user_new[i]}",
        "region": f"{system_attributes_region_new[i]}",
        "role": f"{system_attributes_userType_new[i]}"
    }
    # Отправляем запрос
    profile_api.post(
            "profile/user", params = params)  # Записываем ответ метода POST в переменную response
    
    # Получаем параметр в БД условию
    user_uuid_0_new = params_record_db_condition(dbCursor, "id", "mgp_recipient",
                                                 f"user_id = '{system_attributes_user_new[i]}'")
    
    logging.debug(
            f"Получили из gen_test_user_id_system_attr {system_attributes_user_new[i]} и {user_uuid_0_new}")  # Логируем тело ответа
    
    logging.debug(f"Завершение функции gen_test_user_id_system_attr")  # Логируем тело ответа
    return system_attributes_user_new[i], user_uuid_0_new


# Функция поиска заполненных или генерация заполнения значений системных атрибутов у пользователей
def gen_user_system_attributes(profile_api, dbCursor, i):
    """
    Индексы функции
    2 :
    Получение значений системных атрибутов для указанного пользователя. Прямой сценарий
    3 :
    Обновление значений системных атрибутов для указанного пользователя. Прямой сценарий (Создание)
    Обновление значений системных атрибутов для указанного пользователя. Несуществующий userId
    Обновление значений системных атрибутов для указанного пользователя. Указаны данные со старой информацией
    4 :
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений (1 значение)
    5 :
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений (2 значение)
    """
    logging.debug("Запуск функции gen_user_system_attributes")
    
    # Вызываем функцию генерации user ID для проверки системных атрибутов
    user_id = gen_test_user_id_system_attr(profile_api, dbCursor, i)[0]
    
    # Вызываем функцию генерации системного атрибута
    system_attributes_json_name = gen_system_attributes(profile_api, i)[0]
    
    body = {f"{system_attributes_json_name}": system_attributes_jsonName_value[i]}
    headers = {"Content-Type": "application/json"}
    
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Заполняем атрибут у пользователя
    profile_api.put(
            f"profile/system-attributes/user/{user_id}/set", headers = headers,
            data = body_json)  # Записываем ответ метода GET в переменную response
    
    logging.debug("Завершение функции gen_user_system_attributes")
    
    return user_id, system_attributes_json_name


# Функция поиска заполненных или генерация заполнения значений системных атрибутов у пользователей
def gen_many_user_system_attributes(profile_api, dbCursor, i, user_id = None, counter = 1):
    """
    Индексы функции
    2 :
    Получение значений системных атрибутов для указанного пользователя. Прямой сценарий
    3 :
    Обновление значений системных атрибутов для указанного пользователя. Прямой сценарий (Создание)
    Обновление значений системных атрибутов для указанного пользователя. Несуществующий userId
    4 :
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений (1 значение)
    5 :
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений (2 значение)
    6 :
    Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений, один из них не подходящий
    """
    logging.debug("Запуск функции gen_many_user_system_attributes")
    
    system_attributes_all_json_name = []  # Список для нескольких значений
    
    if user_id is None:
        # Вызываем функцию генерации user ID для проверки системных атрибутов
        user_id = gen_test_user_id_system_attr(profile_api, dbCursor, i)[0]
    
    for A in range(counter):
        # # Вызываем функцию генерации системного атрибута
        # system_attributes_jsonName = gen_system_attributes(profile_api, i)[0]
        
        # Генерируем системный атрибут не функцией, потому что нужно что бы тип пользователя и регион атрибута был
        # у двух атрибутов одинаковый, а через функцию генерации они всегда разные
        
        body = {
            "display": system_attributes_display_new[i],
            "required": system_attributes_required_new[i],
            "name": f"{system_attributes_name_new[i]}",
            # У jsonName:
            # C начала A = 0, поэтому номер i не меняется,
            # затем A = 1, поэтому номер i += 1.
            "jsonName": f"{system_attributes_jsonName_new[i + A]}",
            "fieldOrder": system_attributes_fieldOrder_new[i],
            "fieldType": system_attributes_fieldType_new[i],
            "userType": f"{system_attributes_userType_new[i]}",
            "region": f"{system_attributes_region_new[i]}",
            "metadata": system_attributes_metadata_new[i]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Отправляем запрос
        profile_api.post("/profile/system-attributes/add", headers = headers,
                         data = body_json)  # Записываем ответ метода GET в переменную response
        
        # У jsonName:
        # C начала A = 0, поэтому номер i не меняется,
        # затем A = 1, поэтому номер i += 1.
        body = {f"{system_attributes_jsonName_new[i + A]}": system_attributes_jsonName_value[i]}
        headers = {"Content-Type": "application/json"}
        
        # Парсинг тела запроса
        body_json = parse_request_json(body)[0]  # Парсинг тела запроса
        
        # Заполняем атрибут у пользователя
        profile_api.put(
                f"profile/system-attributes/user/{user_id}/set", headers = headers,
                data = body_json)  # Записываем ответ метода GET в переменную response
        
        # Кладем название системного атрибута в список
        system_attributes_all_json_name.append(system_attributes_jsonName_new[i + A])
        
        logging.debug("Завершение функции gen_many_user_system_attributes")
    return user_id, system_attributes_all_json_name


# Функция поиска файла с ревизиями
def find_file_uuid(dbCursor, i):
    """
    Индексы функции
    1 :
    Получение списка ревизий. Прямой сценарий
    """
    logging.debug('Запуск функции find_file_uuid')
    
    # Получаем параметр в БД условию
    file_uuid, rev = params_record_db_condition_many(dbCursor,
                                                     # SELECT
                                                     "DISTINCT(file_uuid), rev",
                                                     # FROM
                                                     "(SELECT ROW_NUMBER () OVER (), file_uuid, rev FROM public.file_storage_aud WHERE deleted = 'false')x",
                                                     # WHERE
                                                     f"ROW_NUMBER = {i}")
    logging.debug('Завершение функции find_file_uuid')
    return file_uuid, rev


# Функция получения file_uuid, который можно скачать
def find_file_uuid_download(dbCursor, i):
    """Индексы функции.
    1 :
    Скачивание файла base64. Прямой сценарий.
    Скачивание файла. Прямой сценарий.
    Получение метаинформации о загруженном файле. Прямой сценарий."""
    logging.debug('Запуск функции find_file_uuid_download')
    
    # Получаем параметр в БД условию
    file_uuid = params_record_db_condition(dbCursor,
                                           # SELECT
                                           "file_uuid",
                                           # FROM
                                           "(SELECT ROW_NUMBER () OVER (ORDER by file_uuid desc), file_uuid FROM file_storage WHERE deleted = 'false' and expires_on is null ORDER by file_uuid desc)x",
                                           # WHERE
                                           f"ROW_NUMBER = {i}")
    
    logging.debug('Завершение функции find_file_uuid_download')
    
    return file_uuid


# Функция заполнения списка документов у пользователя
def add_new_file_document(profile_api, dbCursor):
    logging.debug('Запуск функции add_new_file_document')
    
    # Ищем пользователя
    user_id_created_by = find_test_user_id(profile_api, dbCursor)[0]
    
    # Кол-во документов, которые хотим загрузить
    i_doc = 5  # Документов
    
    file_uuid = None
    
    # Todo при желании можно сделать файлы разными, пока один и тот же файл
    # Загружаем каждый файл
    for i in range(i_doc):
        params = {
            "createdBy": f"{user_id_created_by}",
        }
        
        files = {
            'file': open(f"{outer_path}/file/success_file.docx",
                         "rb")
        }
        # Отправляем запрос
        profile_api.post(f"/profile/document/upload", params = params, files = files)
        
        # Получаем параметр в БД условию
        file_uuid = params_record_db_condition(dbCursor,
                                               "file_uuid",
                                               "file_storage",
                                               f"created_by = '{user_id_created_by}' ORDER by create_on desc")
    
    logging.debug('Завершение функции add_new_file_document')
    
    # file_uuid отдаем последний
    return user_id_created_by, file_uuid


# Функция подсчета и поиска подходящих атрибутов для конкретного пользователя
def find_list_attributes(dbCursor, user_id, region, user_type, attributes):  # attributes может быть None
    logging.debug('Запуск функции find_list_attributes')
    
    attribute_keys = None
    
    # Если тип пользователя не указан, ищем его
    if user_type is None:
        # Получаем параметр в БД условию
        user_type = params_record_db_condition(dbCursor, "role", "shtp_user",
                                               f"shtp_user_id = '{user_id}'")
    
    # Если регион пользователя не указан, ищем его
    if region is None:
        # Получаем параметр в БД условию
        region = params_record_db_condition(dbCursor, "region", "shtp_user",
                                            f"shtp_user_id = '{user_id}'")
    
    # Получаем количество записей в БД по условию
    # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
    count_base_attribute = count_record_db_condition(dbCursor, 'base_attribute', "deleted = 'False'")
    
    logging.debug(f"Подходящих баз. атрибутов для {user_id}: \n {count_base_attribute}")  # Логируем тело ответа
    
    # Если тип атрибутов BASE
    if attributes == 'BASE':
        attribute_keys = []  # заводим пустой список
        for t in range(count_base_attribute):
            # Получаем параметр в БД условию
            list_base_json_name = params_record_db_condition(dbCursor,
                                                             # SELECT
                                                             "json_name",
                                                             # FROM
                                                             '(SELECT ROW_NUMBER () OVER (ORDER BY json_name COLLATE "POSIX"), json_name FROM base_attribute '
                                                             "WHERE deleted = 'False' ORDER BY json_name)x",
                                                             # WHERE
                                                             f'ROW_NUMBER = {t + 1} ORDER by json_name COLLATE "POSIX"')
            attribute_keys.append(list_base_json_name)  # добавляем его в список
        logging.debug(f"Ключи названий базовых атрибутов {attribute_keys}")  # Логируем тело ответа
    
    # Получаем количество записей в БД по условию
    # В функцию count_record_db_condition отдаем dbCursor - коннект к БД, название таблицы 'table', и условие то что идет после WHERE - 'condition'
    count_add_attribute = count_record_db_condition(dbCursor, 'additional_attribute',
                                                    f"user_type LIKE '%{user_type}%' and (region is null or region = '{region}' or region = '')")
    
    logging.debug(
            f"Подходящих доп. атрибутов для {user_id} с регионом {region} или не указанным и типом пользователя {user_type}:\n"
            f"{count_add_attribute}")  # Логируем тело ответа
    
    # Если тип атрибутов ADDITIONAL
    if attributes == 'ADDITIONAL':
        
        # Выгружаем список ключей названий доп. атрибутов
        attribute_keys = []  # заводим пустой список
        for t in range(count_add_attribute):
            # Получаем параметр в БД условию
            list_add_json_name = params_record_db_condition(dbCursor,
                                                            # SELECT
                                                            "json_name",
                                                            # FROM
                                                            f"(SELECT ROW_NUMBER () OVER (ORDER BY id), json_name FROM additional_attribute WHERE user_type LIKE '%{user_type}%' and (region is null or region = '' or region = '{region}'))x",
                                                            f"ROW_NUMBER = {t + 1}")
            attribute_keys.append(list_add_json_name)  # добавляем его в список
        logging.debug(f"Ключи названий доп. атрибутов {attribute_keys}")  # Логируем тело ответа
    
    # Получаем кол-во всех атрибутов
    count_attributes = count_add_attribute + count_base_attribute
    
    # Если тип атрибутов не указан, то проверяются все
    if attributes is None:
        # Выгружаем список ключей названия атрибутов
        attribute_keys = []  # заводим пустой список
        for t in range(count_attributes):
            # Получаем параметр в БД условию
            full_list = params_record_db_condition(dbCursor,
                                                   # SELECT
                                                   "json_name",
                                                   # FROM
                                                   '(SELECT ROW_NUMBER () OVER (ORDER by json_name COLLATE "POSIX"), * FROM '
                                                   "(SELECT json_name FROM base_attribute WHERE deleted = 'False' "
                                                   "UNION "
                                                   f"SELECT json_name FROM additional_attribute WHERE user_type LIKE '%{user_type}%' and (region is null or region = '{region}' or region = '') )b "
                                                   f'ORDER by json_name COLLATE "POSIX")c',
                                                   # WHERE
                                                   f'ROW_NUMBER = {t + 1}')
            logging.debug(f"Ключ № {t} - {full_list}")  # Логируем тело ответа
            attribute_keys.append(full_list)  # добавляем его в список
        logging.debug(f"Все ключи названий атрибутов - {attribute_keys}")  # Логируем тело ответа
    
    logging.debug('Завершение функции find_list_attributes')
    
    return count_base_attribute, count_add_attribute, attribute_keys


#  Функция установки статуса для поиска пользователя по статусу
def gen_test_status_shtp(profile_api, dbCursor):
    logging.debug('Запуск функции gen_test_status_shtp')
    
    # Номер итерации для генерации данных profile_user_<param>_new (Для создания)
    i = 5
    
    # Функция поиска пользователя, его региона и типа, с заполненным атрибутом
    user_id, region, user_type = find_test_user_id_data_constructor(profile_api, dbCursor, i)
    
    body = {
        "userId": f'{user_id}',
        "region": region,
        "role": f"{user_type}",
        "status": {
            "status": f"{profile_users_user_id_status}",
            "documentLink": f"{profile_users_user_id_documentLink}"
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    # Парсинг тела запроса
    body_json = parse_request_json(body)[0]  # Парсинг тела запроса
    
    # Отправляем запрос
    profile_api.patch(
            f"profile/user/{user_id}", headers = headers,
            data = body_json)  # Записываем ответ метода POST в переменную response
    
    logging.debug('Завершение функции gen_test_status_shtp')
    return profile_users_user_id_status, region
