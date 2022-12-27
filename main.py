from classes import HH, SuperJob, HHVacancy, SJVacancy
from utils import sorting, get_top, clean_directory


def main():
    user_input = input("Введите сервис подбора вакансий [HH, SuperJob]:")
    user_input_keyword = input("Введите слово для поиска:")
    user_input_count = input("Сколько необходимо вывести вакансий?")
    user_input_sorting = input("Вы хотите отсортировать вакансии по зарплате? [Yes/No]")
    while True:
        if user_input == 'HH':
            hh_engine = HH()
            key_word = user_input_keyword
            vacancies_count = 1000
            hh_res = hh_engine.get_request(key_word, vacancies_count)
            hh_data = HH.get_connector('hh_res.json')
            hh_data.insert(hh_res)
            HHVacancy.read_data('hh_res.json')
            if user_input_sorting == 'No' or 'no':
                get_top(HHVacancy.hh_vacancies, int(user_input_count))
                print(f'{HHVacancy.get_count_of_vacancy} - количество вакансий от текущего сервиса')
            if user_input_sorting == 'Yes' or 'yes':
                get_top(sorting(HHVacancy.hh_vacancies), int(user_input_count))
                print(f'{HHVacancy.get_count_of_vacancy} - количество вакансий от текущего сервиса')
        if user_input == 'SuperJob':
            sj_engine = SuperJob()
            key_word = user_input_keyword
            vacancies_count = 1000
            sj_res = sj_engine.get_request(key_word, vacancies_count)
            sj_data = SuperJob.get_connector('sj_res.json')
            sj_data.insert(sj_res)
            SJVacancy.read_data('sj_res.json')
            if user_input_sorting == 'No' or 'no':
                get_top(SJVacancy.sj_vacancies, int(user_input_count))
                print(f'{SJVacancy.get_count_of_vacancy} - количество вакансий от текущего сервиса')
            if user_input_sorting == 'Yes' or 'yes':
                get_top(sorting(SJVacancy.sj_vacancies), int(user_input_count))
                print(f'{SJVacancy.get_count_of_vacancy} - количество вакансий от текущего сервиса')

        break


if __name__ == '__main__':
    main()
    clean_directory()
