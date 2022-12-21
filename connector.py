import json
import logging
import os


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, data_file):
        self.__data_file = data_file

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        """
        try:
            if self.__data_file not in os.listdir('.'):
                with open(self.__data_file, 'w') as file:
                    json.dump([], file)
        except Exception as ex:
            logging.critical(ex)
        return self.__data_file

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, 'r+') as f:
            json.dump(data, f)
        return self.__data_file

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """

        data_from_file = {}
        with open(self.__data_file, 'r+') as file:
            data = json.load(file)
            if not query:
                return [data]
            for d in data:
                for k, v in query.items():
                    if d[k] == v:
                        data_from_file.update(d)
        return data_from_file

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select
        """
        try:
            with open(self.__data_file, 'r') as f:
                data = json.loads(f.read())

            with open(self.__data_file, 'w') as f:
                result = None

                for key in query.keys():
                    result = [*filter(lambda el: el[key] != query[key], result if result else data)]

                json.dump(result, f)

        except Exception as ex:
            logging.critical(ex)
