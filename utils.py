import os


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    return sorted(vacancies, reverse=True)


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    try:
        for i in range(top_count):
            print(vacancies[i])
    except IndexError:
        print(f'Нет такого количества вакансий')


def clean_directory():
    if os.path.exists('hh_res.json'):
        os.remove('hh_res.json')
    if os.path.exists('sj_res.json'):
        os.remove('sj_res.json')
