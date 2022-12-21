import requests
from abc import ABC, abstractmethod
# import json


class Vacancy:
    class Vacancy:
        __slots__ = ('name', 'link', 'description', 'salary')

        def __init__(self, name, link, description, salary):
            self.name = name
            self.link = link
            self.description = description
            self.salary = salary

        def __str__(self):
            return f'{self.name} - {self.link}\n{self.description}\n{self.salary}'


class Engine(ABC):
    @abstractmethod
    def get_request(self, key_word, vacancies_count):
        return key_word, vacancies_count

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    __url = 'https://api.hh.ru'
    __per_page = 20

    def _get_vacancies(self, key_word, page):
        response = requests.get(f'{self.__url}/vacancies?text={key_word}&page={page}')
        if response.status_code == 200:
            return response.json()
        return None

    def get_request(self, key_word, vacancies_count):
        page = 0
        result = []
        while self.__per_page * page < vacancies_count:
            tmp_result = self._get_vacancies(key_word, page)
            if tmp_result:
                result += tmp_result.get('items')
                page += 1
            else:
                break
        return result


class SuperJob(Engine):
    __url = 'https://api.superjob.ru/2.0'
    __secret = 'v3.r.137220932.1fac36ffcaca135a29c6a295a45e060ea37cf1af.8501aa108268e3b187e8ff6ecab5d400dd7ba5fa'
    __per_page = 20

    def _get_vacancies(self, key_word, page):
        url = f'{self.__url}/vacancies/?page={page}&keyword={key_word}'
        headers = {'X-Api-App-Id': self.__secret,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_request(self, key_word, vacancies_count):
        page = 0
        result = []
        while self.__per_page * page < vacancies_count:
            tmp_result = self._get_vacancies(key_word, page)
            if tmp_result:
                result += tmp_result.get('objects')
                page += 1
            else:
                break
        return result


# if __name__ == '__main__':
    # sj_engine = SuperJob()
    # key_word = 'kotlin'
    # vacancies_count = 100
    #
    # sj_res = sj_engine.get_request(key_word, vacancies_count)
#     hh_engine = HH()
#     key_word = 'kotlin'
#     vacancies_count = 100
#     res = hh_engine.get_request(key_word, vacancies_count)
#
    # with open('sj_res.json', 'w', encoding='utf-8') as res_file:
    #     json.dump(sj_res, res_file)
#
#     with open('res.json', 'r', encoding='utf-8') as res_file:
#         res_data = json.load(res_file)
#         for item in res_data:
#             print(f"{item.get('name')}, {item.get('salary')}, {item['area'].get('name')}")
