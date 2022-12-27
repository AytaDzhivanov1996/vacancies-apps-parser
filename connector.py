import os
import json


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __init__(self, df):
        self.__data_file = df
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        """
        if self.__data_file not in os.listdir('.'):
            with open(self.__data_file, 'w') as file:
                json.dump([], file)
        else:
            return self.__data_file

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, 'r') as f:
            files = json.load(f)
            files.append(data)

        with open(self.__data_file, 'w') as f:
            json.dump(files, f)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """

        data_in_file = []
        with open(self.__data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not query:
            return data

        for d in data:
            for k, v in query.items():
                if d[k] == v:
                    data_in_file.append(d)
        return data_in_file

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select
        """
        with open('df.json', 'r') as f:
            data = json.load(f)

        with open('df.json', 'w') as f:
            result = None

            for key in query.keys():
                result = [*filter(lambda el: el[key] != query[key], result if result else data)]
            json.dump(result, f)
