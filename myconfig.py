import random
import string
import uuid

# Подключение к API
from datetime import datetime

URL_SERVER = "jk01.tr.local"
URL_PORT = "30335"
URL = f"http://{URL_SERVER}:{URL_PORT}/"

# Подключение к БД
SERVER = ''  # Сервер, где находится БД
PORT = 'XXXX'
DATABASE = ''  # Имя БД
USER = ''  # Имя пользователя БД
PASSWORD = ''  # Пароль пользователя БД

# Для поиска репозитория запуска автотестов
outer_path = 'C:/SVN_APK_NA_VIGRUZKU/profile-service/01/07/'

# Переменные
# Общее

empty_value = ''

############################################################################################################
# Для методов "Управление группами аттрибутов"

# Для запуска методов /group/name
group_block_wrong = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
group_name_wrong = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
group_role_wrong = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
group_attr_name_wrong = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))

role = ['B', 'L', 'A', 'P']  # B-ИП L-ЮЛ A-ОГВ P-ФЛ

group_gen_role = [random.choice(role),
                  random.choice(role), random.choice(role), random.choice(role), random.choice(role),
                  random.choice(role)]

'''
Индексы функции
0 :
Обновить группу. Прямой сценарий (Создать).
Получить данные о группе. Прямой сценарий.
Получить список атрибутов входящих в группу. Прямой сценарий.
Добавить атрибуты в группу. Прямой сценарий - Добавление 1 атрибута (Создание группы).
1 :
Получить список атрибутов входящих в группу. Прямой сценарий
Получить список атрибутов входящих в группу. Несуществующий block.
Получить список атрибутов входящих в группу. Не указан block.
2 :
Создать группу. Прямой сценарий
Создать группу. Такая группа атрибутов уже существует по name
3 : Обновить группу. Прямой сценарий (Обновить)
4 :
Создать группу. Некорректные данные группы атрибутов
5 :
Создать группу. Разные типы ролей ().
6 :
Создать группу. Разные типы ролей
7 :
Создать группу. Разные типы ролей
8 :
Создать группу. Разные типы ролей.
'''
# Для функции создания группы
group_gen_name = [f"test_GROUP_name_{random.randint(5000, 999999999)}",
                  f"test_GROUP_name_{random.randint(5000, 999999999)}",
                  f"test_GROUP_name_{random.randint(5000, 999999999)}",
                  f"test_GROUP_name_{random.randint(5000, 999999999)}",
                  f"test_GROUP_name_{random.randint(5000, 999999999)}",
                  f"test_GROUP_name_{random.randint(5000, 999999999)}",
                  f"test_GROUP_name_{random.randint(5000, 999999999)}",
                  f"test_GROUP_name_{random.randint(5000, 999999999)}",
                  f"test_GROUP_name_{random.randint(5000, 999999999)}"]
group_gen_description = f"test_group_description_{random.randint(5000, 999999999)}"
# group_gen_position = random.randint(0, 999)
group_gen_block = f"test_GROUP_BLOCK_{random.randint(5000, 999999999)}"  # Не удалять

# Индексы функции
# 0 - Удалить группу. Прямой сценарий
# 1 - Удалить список атрибутов из группы. Прямой сценарий
# 2 - Удалить список атрибутов из группы. Не указывать тело запроса
# 3 - Удалить список атрибутов из группы. Атрибута нет в группе

# Для функции создания группы, для ее последующего удаления
group_gen_del_name = [f"test_DEL_GROUP_{random.randint(5000, 999999999)}",
                      f"test_DEL_GROUP_{random.randint(5000, 999999999)}",
                      f"test_DEL_GROUP_{random.randint(5000, 999999999)}",
                      f"test_DEL_GROUP_{random.randint(5000, 999999999)}"]
group_gen_del_description = f"DEL_description_{random.randint(5000, 999999999)}"
group_gen_del_position = random.randint(0, 999)
group_gen_del_block = f"test_DEL_GROUP_BLOCK_{random.randint(5000, 999999999)}"  # Не удалять

# Список параметров для сверки один, т.к. ключи БД и JSON одинаковые
param_ALL_group = ["name", "description", "role"]
#
# Список параметров для сверки
param_ALL_group_link = {"attrName": "attr_name",
                        "position": "position",
                        "block": "block"}

################################################################################################################################################################

# Для методов "Управление атрибутами"

# Todo подумать об объединении переменных wrong в одну(во всем файле)
# Для запуска методов /profile/attributes/base/
base_attribute_id_wrong = random.randint(50000000, 99999999999)
base_attribute_id_wrong_str = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
base_attribute_name_wrong = random.randint(5000, 99999)
base_attribute_identity_wrong = random.randint(5000, 99999)
base_attribute_json_Name_wrong = random.randint(5000, 99999)
base_attribute_type_wrong = random.randint(5000, 99999)
base_attribute_metadata_wrong = random.randint(5000, 99999)
base_attribute_creationData_wrong = "2022-111-111T10:18:19.333+00:00"
full_attribute_value_new = random.randint(0, 5000)

# 1 - Обновление данных пользователя, сотрудником РОУ АПК. Прямой сценарий
base_attribute_id_new = [random.randint(50000, 99999), random.randint(50000, 99999), random.randint(50000, 99999),
                         random.randint(50000, 99999), random.randint(50000, 99999),
                         random.randint(50000, 99999), random.randint(50000, 99999),
                         random.randint(50000, 99999)]
base_attribute_identity_new = [f"test_BASE_identity_{random.randint(5000, 9999)}",
                               f"test_BASE_identity_{random.randint(50000, 99999)}",
                               f"test_BASE_identity_{random.randint(5000, 9999)}",
                               f"test_BASE_identity_{random.randint(5000, 9999)}",
                               f"test_BASE_identity_{random.randint(5000, 9999)}",
                               f"test_BASE_identity_{random.randint(5000, 9999)}",
                               f"test_BASE_identity_{random.randint(50000, 99999)}",
                               f"test_BASE_identity_{random.randint(5000, 9999)}",
                               f"test_BASE_identity_{random.randint(50000, 99999)}"]
base_attribute_name_new = [f"test_BASE_name_{random.randint(5000, 9999)}",
                           f"test_BASE_name_{random.randint(50000, 99999)}",
                           f"test_BASE_name_{random.randint(50000, 99999)}",
                           f"test_BASE_name_{random.randint(5000, 9999)}",
                           f"test_BASE_name_{random.randint(5000, 9999)}",
                           f"test_BASE_name_{random.randint(5000, 9999)}",
                           f"test_BASE_name_{random.randint(50000, 99999)}",
                           f"test_BASE_name_{random.randint(5000, 9999)}",
                           f"test_BASE_name_{random.randint(50000, 99999)}"]
base_attribute_json_name_new = [f"test_BASE_json_name_{random.randint(5000, 9999)}",
                                f"test_BASE_json_name_{random.randint(50000, 99999)}",
                                f"test_BASE_json_name_{random.randint(5000, 9999)}",
                                f"test_BASE_json_name_{random.randint(5000, 9999)}",
                                f"test_BASE_json_name_{random.randint(5000, 9999)}",
                                f"test_BASE_json_name_{random.randint(5000, 9999)}",
                                f"test_BASE_json_name_{random.randint(50000, 99999)}",
                                f"test_BASE_json_name_{random.randint(5000, 9999)}",
                                f"test_BASE_json_name_{random.randint(50000, 99999)}"]
base_attribute_type_new = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # TODO узнать обозначение этих типов и откуда они берутся
base_attribute_deleted_new = [False, False, False, False, False, False, False, False, False,
                              False]  # TODO может быть нужно рандомизировать
base_attribute_metadata_new = [{'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}},
                               {'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}},
                               {'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}},
                               {'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}}]

# Список параметров для сверки
param_ALL_base_attribute = {"id": "id", "deleted": "deleted", "identity": "identity", "jsonName": "json_Name",
                            "name": "name", "type": "type",
                            "metadata": "metadata",
                            "creationDate": "creation_date"}  # Задаем список параметров, которые будем сверять.

param_ALL_base_attribute_search = {
    "content": {
        "id": "id",
        "deleted": "deleted",
        "identity": "identity",
        "jsonName": "json_Name",
        "name": "name",
        "type": "type",
        "metadata": "metadata",
        "creationDate": "creation_date"
    },
    "empty": "",
    "first": "",
    "last": "",
    "number": "",
    "numberOfElements": "",
    "pageable": {
        "offset": "",
        "pageNumber": "",
        "pageSize": "",
        "paged": "",
        "sort": {
            "empty": "",
            "sorted": "",
            "unsorted": ""
        },
        "unpaged": ""
    },
    "size": "",
    "sort": {
        "empty": "",
        "sorted": "",
        "unsorted": ""
    },
    "totalElements": "",
    "totalPages": ""
}

#################################################

invalid_symbol = "!@#$%^*()_:;?/>.<,"

# Для запуска методов /profile/attributes/additional/
additional_attribute_id_wrong = random.randint(5000, 999999)
additional_attribute_id_wrong_str = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
additional_attribute_json_name_wrong_str = invalid_symbol[:5]
additional_attribute_name_wrong = random.randint(0, 999999)
additional_attribute_jsonNames_wrong = random.randint(0, 99999)

'''
Индекс генерации и использования данных
0 :
Добавление дополнительных атрибутов получателей МГП. Прямой сценарий
Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по name (Этот Name)
Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по jsonName (Этот jsonName)
1 :
Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по name (Эти ост. параметры)
2 :
Добавление дополнительных атрибутов получателей МГП. Такой дополнительный атрибут уже существует по jsonName (Эти ост. параметры)
3 :
Добавление дополнительных атрибутов получателей МГП. В теле не указан jsonName
3 :
Добавление дополнительных атрибутов получателей МГП. В теле не указан Name
4 :
Обновление данных дополнительного атрибута. Прямой сценарий (Это создаем)
5 :
Обновление данных дополнительного атрибута. Прямой сценарий (На это обновляем)
6 :
Добавление дополнительных атрибутов получателей МГП. Некорректные данные поля userType
Добавление дополнительных атрибутов получателей МГП. Некорректные данные поля region
Добавление дополнительных атрибутов получателей МГП. Некорректные данные поля userType
Добавление дополнительных атрибутов получателей МГП. Некорректные данные поля creationDate
7 :
Получить список атрибутов входящих в группу. Прямой сценарий
8 :
Обновление данных дополнительного атрибута. Использовать jsonName в качестве идентификатора (На это обновляем)
9 :
Обновление данных дополнительного атрибута. Некорректный id
10 :
Добавить атрибуты в группу. Такие данные уже есть в системе.
Добавить атрибуты в группу. Прямой сценарий - Добавление 1 атрибута.
Обновление данных дополнительного атрибута. Указаны не все поля в теле запроса (Для additional_attribute_name_new и additional_attribute_userType_new)
11 :
Добавить атрибуты в группу. Добавление нескольких атрибутов
'''
additional_attribute_display_new = [True, False,
                                    random.choice([True, False]), random.choice([True, False]),
                                    random.choice([True, False]), random.choice([True, False]),
                                    random.choice([True, False]), random.choice([True, False]),
                                    random.choice([True, False]), random.choice([True, False]),
                                    random.choice([True, False]), random.choice([True, False]),
                                    random.choice([True, False])]
additional_attribute_required_new = [True, False, False, False, False, False, False, False, False, False, False, False]
additional_attribute_name_new = [f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}',
                                 f'test_ADDITIONAL_name_{random.randint(1000000, 9999999)}']
additional_attribute_jsonName_new = [f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}',
                                     f'test_ADDITIONAL_json_name_{random.randint(1000000, 9999999)}']
additional_attribute_fieldOrder_new = [random.randint(1000, 9999), random.randint(1000, 9999),
                                       random.randint(1000, 9999), random.randint(1000, 9999),
                                       random.randint(1000, 9999), random.randint(1000, 9999),
                                       random.randint(1000, 9999), random.randint(1000, 9999),
                                       random.randint(1000, 9999), random.randint(1000, 9999),
                                       random.randint(1000, 9999), random.randint(1000, 9999),
                                       random.randint(1000, 9999), random.randint(1000, 9999),
                                       random.randint(1000,
                                                      9999)]  # TODO узнать что за значения принимает, и на что влияет
additional_attribute_fieldType_new = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                      1]  # TODO узнать что за значения принимает, и на что влияет
additional_attribute_userType_new = ['L', 'L', 'L', 'L', 'L', 'L', f'{group_gen_role[0]}',
                                     f'{group_gen_role[1]}', 'L', 'L', group_gen_role[0],
                                     group_gen_role[4]]  # TODO рандомизировать по надобности
# group_gen_role 0 и 1 для добавлений в группу и совпадении по роли
additional_attribute_region_new = [random.randint(10, 99), random.randint(10, 99), random.randint(10, 99),
                                   random.randint(10, 99), random.randint(10, 99),
                                   random.randint(10, 99), random.randint(10, 99),
                                   random.randint(10, 99), random.randint(10, 99),
                                   random.randint(10, 99), random.randint(10, 99),
                                   random.randint(10, 99), random.randint(10, 99)]
additional_attribute_creationDate_new = [datetime.now().isoformat(), datetime.now().isoformat(),
                                         datetime.now().isoformat(), datetime.now().isoformat(),
                                         datetime.now().isoformat(), datetime.now().isoformat(),
                                         datetime.now().isoformat(), datetime.now().isoformat(),
                                         datetime.now().isoformat(), datetime.now().isoformat(),
                                         datetime.now().isoformat(), datetime.now().isoformat(),
                                         datetime.now().isoformat()]
additional_attribute_metadata_new = [{'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}},
                                     {'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}},
                                     {'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}},
                                     {'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}},
                                     {'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}},
                                     {'additionalProp1': {}}, {'additionalProp1': {}}, {'additionalProp1': {}}]

# Для метода (Добавление дополнительных атрибутов получателей МГП)
# Для проверок:
# Некорректные данные дополнительного атрибута
additional_attribute_name_new_wrong = f'test_ADDITIONAL_WRONG_{random.randint(1000000, 9999999)}'
additional_attribute_display_new_wrong = random.choice(['Tru2e', 'Fal2se'])
additional_attribute_required_new_wrong = 'Far45lse'
additional_attribute_jsonName_new_wrong = f'test_ADDITIONAL_WRONG_json_name_{random.randint(1000000, 9999999)}'
additional_attribute_fieldOrder_new_wrong = random.randint(1000, 9999)
additional_attribute_fieldType_new_wrong = 143432
additional_attribute_userType_new_wrong = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
additional_attribute_region_new_wrong = random.randint(100, 992)
additional_attribute_creationDate_new_wrong = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
additional_attribute_metadata_new_wrong = {"additionalProp1": {}, }
#
param_ALL_additional_attribute = {"id": "id", "display": "display",
                                  "required": "required",
                                  "jsonName": "json_Name",
                                  "name": "name",
                                  "fieldOrder": "field_order",
                                  "fieldType": "field_type",
                                  "userType": "user_type",
                                  "region": "region",
                                  "metadata": "metadata",
                                  "creationDate": "creation_date"}  # Задаем список параметров, которые будем сверять. Тут ключи БД

param_ALL_additional_attribute_search = {
    "content": {
        "id": "id",
        "display": "display",
        "required": "required",
        "jsonName": "json_Name",
        "name": "name",
        "fieldOrder": "field_order",
        "fieldType": "field_type",
        "userType": "user_type",
        "region": "region",
        "metadata": "metadata",
        "creationDate": "creation_date"
    },
    "empty": "",
    "first": "",
    "last": "",
    "number": "",
    "numberOfElements": "",
    "pageable": {
        "offset": "",
        "pageNumber": "",
        "pageSize": "",
        "paged": "",
        "sort": {
            "empty": "",
            "sorted": "",
            "unsorted": ""
        },
        "unpaged": ""
    },
    "size": "",
    "sort": {
        "empty": "",
        "sorted": "",
        "unsorted": ""
    },
    "totalElements": "",
    "totalPages": ""
}

#######################################################################################################################################################################

# Для запуска методов /profile/system-attributes/
system_attributes_id_int_wrong = random.randint(5000, 999999)
system_attributes_id_wrong = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
system_attributes_names_wrong = random.randint(5000, 999999)
system_attributes_jsonNames_wrong = random.randint(5000, 999999)
system_attributes_userId_wrong = random.randint(5000, 999999)
system_attributes_wrong = random.randint(5000, 999999)

'''
Индексы функции
0 :
Получение системного атрибута по его json name. Прямой сценарий
Изменение системного атрибута. Прямой сценарий (Создание)
1 :
Изменение системного атрибута. Прямой сценарий (Обновление)
Получение системного атрибута по идентификатору. Прямой сценарий
Получение существующих системных атрибутов. Прямой сценарий
Получение существующих системных атрибутов. Указан только jsonNames
Получение существующих системных атрибутов. Указан только jsonNames
Получение существующих системных атрибутов. Некорректный jsonNames
Получение существующих системных атрибутов. Некорректный names
Удаление системного атрибута. Прямой сценарий
2 :
Получение значений системных атрибутов для указанного пользователя. Прямой сценарий
3 :
Добавление системного атрибута. Прямой сценарий
4 :
Добавить атрибуты в группу. Добавление нескольких атрибутов
Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений
5 :
Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений
6 :
Добавление системного атрибута. Некорректные данные поля userType
Добавление системного атрибута. Некорректные данные поля region
Обновление значений системных атрибутов для указанного пользователя. Тип пользователя и system_attributes разные
'''
system_attributes_display_new = [random.choice([True, False]), random.choice([True, False]),
                                 random.choice([True, False]), random.choice([True, False]),
                                 random.choice([True, False]), random.choice([True, False]),
                                 random.choice([True, False])]
system_attributes_required_new = [True, False, False, False, False, False, False, False]
system_attributes_name_new = [f'test_SYSTEM_name_{random.randint(5000, 999999)}',
                              f'test_SYSTEM_name_{random.randint(5000, 999999)}',
                              f'test_SYSTEM_name_{random.randint(5000, 999999)}',
                              f'test_SYSTEM_name_{random.randint(5000, 999999)}',
                              f'test_SYSTEM_name_{random.randint(5000, 999999)}',
                              f'test_SYSTEM_name_{random.randint(5000, 999999)}',
                              f'test_SYSTEM_name_{random.randint(5000, 999999)}']
system_attributes_jsonName_new = [f'test_SYSTEM_json_name_{random.randint(5000, 999999)}',
                                  f'test_SYSTEM_json_name_{random.randint(5000, 999999)}',
                                  f'test_SYSTEM_json_name_{random.randint(5000, 999999)}',
                                  f'test_SYSTEM_json_name_{random.randint(5000, 999999)}',
                                  f'test_SYSTEM_json_name_{random.randint(5000, 999999)}',
                                  f'test_SYSTEM_json_name_{random.randint(5000, 999999)}',
                                  f'test_SYSTEM_json_name_{random.randint(5000, 999999)}']
system_attributes_fieldOrder_new = [random.randint(5000, 9999), random.randint(5000, 9999), random.randint(5000, 9999),
                                    random.randint(5000, 9999), random.randint(5000, 9999), random.randint(5000, 9999),
                                    random.randint(5000, 9999), random.randint(5000, 9999)]
system_attributes_fieldType_new = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

system_attributes_userType_new = ['L', group_gen_role[1], 'L', 'L', group_gen_role[4], 'L', 'A', 'L']
system_attributes_region_new = [random.randint(10, 99), random.randint(10, 99), random.randint(10, 99),
                                random.randint(10, 99), random.randint(10, 99), random.randint(10, 99),
                                random.randint(10, 99), random.randint(10, 99), random.randint(10, 99),
                                random.randint(10, 99)]
system_attributes_metadata_new = [{"additionalProp1": {}, }, {"additionalProp1": {}, }, {"additionalProp1": {}, },
                                  {"additionalProp1": {}, }, {"additionalProp1": {}, }, {"additionalProp1": {}, },
                                  {"additionalProp1": {}, }, {"additionalProp1": {}, }]

system_attributes_user_new = [f"test_USERID_{random.randint(50500, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}"
                              f"test_USERID_{random.randint(5000, 999999999)}",
                              f"test_USERID_{random.randint(5000, 999999999)}"
                              ]
# Для генерации нового
system_attributes_userType = random.choice(role)
system_attributes_region = random.randint(10, 99)
'''
0 :
Обновление значений системных атрибутов для указанного пользователя. Несуществующий additionalProp (Обновление)
1 :
Обновление значений системных атрибутов для указанного пользователя. Несуществующий userId (Обновление)
2 :
3 :
Обновление значений системных атрибутов для указанного пользователя. Прямой сценарий (Создание)
Обновление значений системных атрибутов для указанного пользователя. Несуществующий additionalProp (Создание)
Обновление значений системных атрибутов для указанного пользователя. Несуществующий userId (Создание)
4 :
Обновление значений системных атрибутов для указанного пользователя. Прямой сценарий (Обновление)
Обновление значений системных атрибутов для указанного пользователя. Указаны данные со старой информацией
5 :
Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений
6 :
Обновление значений системных атрибутов для указанного пользователя. Обновление нескольких значений
'''
system_attributes_jsonName_value = [random.randint(1000, 9999), random.randint(1000, 9999), random.randint(1000, 9999),
                                    random.randint(1000, 9999),
                                    random.randint(1000, 9999),
                                    random.randint(1000, 9999),
                                    random.randint(1000, 9999),
                                    random.randint(1000, 9999),
                                    random.randint(1000, 9999),
                                    random.randint(1000, 9999)]

####################################################################################################################################################################
# Словари param_ALL_system_attribute и param_ALL_system_attribute_add одинаковые, таблица одна и та же, объединила в один
param_ALL_system_attribute = {"id": "id",
                              "required": "required",
                              "jsonName": "json_Name",
                              "name": "name",
                              "fieldType": "field_type",
                              "userType": "user_type",
                              "region": "region",
                              "metadata": "metadata",
                              'creationDate': "creation_date"
                              }

param_ALL_user_system_attribute = "value"  # ,"creation_date"]  # Задаем список параметров, которые будем сверять. Тут ключи БД

########################################################################################################################################################################
