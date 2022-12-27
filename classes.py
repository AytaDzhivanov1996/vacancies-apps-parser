import requests
from abc import ABC, abstractmethod
from connector import Connector
import json


class Engine(ABC):
    @abstractmethod
    def get_request(self, key_word, vacancies_count):
        return key_word, vacancies_count

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        exemplar = Connector(file_name)
        return exemplar


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


class Vacancy:
    class_name = 'Vacancy'
    __slots__ = ('name', 'link', 'salary')

    def __init__(self, name, link, salary):
        self.name = name
        self.link = link
        self.salary = salary
        self.class_name = Vacancy.class_name

    def salary_check(self, other):
        if not self.salary:
            self.salary = 0
        if not other.salary:
            other.salary = 0
        return self.salary, other.salary

    def __repr__(self):
        if self.salary:
            return f"{self.class_name}: {self.company_name}, зарплата: {self.salary} руб/мес"
        else:
            return f"{self.class_name}: {self.company_name}, зарплата: нет данных"

    def __eq__(self, other):
        self.salary_check(other)
        return self.salary == other.salary

    def __ne__(self, other):
        self.salary_check(other)
        return self.salary != other.salary

    def __gt__(self, other):
        self.salary_check(other)
        return self.salary > other.salary

    def __ge__(self, other):
        self.salary_check(other)
        return self.salary >= other.salary

    def __lt__(self, other):
        self.salary_check(other)
        return self.salary < other.salary

    def __le__(self, other):
        self.salary_check(other)
        return self.salary <= other.salary

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(HHVacancy.hh_vacancies):
            x = HHVacancy.hh_vacancies[self.current_index]
            self.current_index += 1
            return x
        else:
            raise StopIteration


class CounterMixin:
    """
    Вернуть количество вакансий от текущего сервиса.
    Получать количество необходимо динамически из файла.
    """
    @property
    def get_count_of_vacancy(self):
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        return len(data)


class HHVacancy(CounterMixin, Vacancy):
    """ HeadHunter Vacancy """
    hh_vacancies = []
    class_name = 'HH'
    data_file = 'hh_res.json'

    def __init__(self, name, link, salary, company_name):
        super().__init__(name, link, salary)
        self.company_name = company_name
        self.class_name = HHVacancy.class_name
        self.data_file = HHVacancy.data_file

    @classmethod
    def read_data(cls, data_file):
        with open(f'{data_file}') as f:
            data = json.load(f)
            for elem in data:
                for i in elem:
                    name = i.get('name')
                    link = i.get('url')
                    try:
                        if i.get('salary').get('currency') == 'USD':
                            salary = i.get('salary').get('from') * 70
                        elif i.get('salary').get('currency') == 'EUR':
                            salary = i.get('salary').get('from') * 75
                        else:
                            salary = i.get('salary').get('from')
                    except (AttributeError, TypeError):
                        salary = 0
                    company_name = i.get('employer').get('name')

                    cls.hh_vacancies.append(HHVacancy(name, link, salary, company_name))


class SJVacancy(CounterMixin, Vacancy):
    """ SuperJob Vacancy """
    sj_vacancies = []
    class_name = 'SJ'
    data_file = 'sj_res.json'

    def __init__(self, name, link, salary, company_name):
        super().__init__(name, link, salary)
        self.company_name = company_name
        self.class_name = SJVacancy.class_name
        self.data_file = SJVacancy.data_file

    @classmethod
    def read_data(cls, data_file):
        with open(f'{data_file}') as f:
            data = json.load(f)
            for elem in data:
                for i in elem:
                    name = i.get('profession')
                    link = i.get('link')
                    try:
                        salary = i.get('payment_from')
                    except (AttributeError, TypeError):
                        salary = 0
                    company_name = i.get('firm_name')

                    cls.sj_vacancies.append(SJVacancy(name, link, salary, company_name))
