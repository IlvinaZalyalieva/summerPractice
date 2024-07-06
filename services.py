import requests
from datetime import datetime
import importlib.resources as pkg_resources
import sql  

def read_sql_file(filename):
    with pkg_resources.open_text(sql, filename) as file:
        return file.read()
    

def parse_vacancies():
    url = 'https://api.hh.ru/vacancies'
    response = requests.get(url)
    vacancies = response.json().get('items', [])
    return vacancies

def save_vacancies_to_db(conn, vacancies):
    cursor = conn.cursor()
    cursor.execute(read_sql_file('create_table.sql'))
    insert_query = read_sql_file('insert_vacancy.sql')
    for vacancy in vacancies:
        published_at = datetime.strptime(vacancy['published_at'], '%Y-%m-%dT%H:%M:%S%z').date()
        data = (
            vacancy['name'],
            vacancy['area'].get('name'),
            vacancy['salary']['currency'] if vacancy.get('salary') else None,
            vacancy['salary']['from'] if vacancy.get('salary') else None,
            vacancy['salary']['to'] if vacancy.get('salary') else None,
            vacancy['employer'].get('name'),
            vacancy['employer'].get('id'),
            vacancy['snippet'].get('requirement'),
            vacancy['snippet'].get('responsibility'),
            datetime.now().date(),
            published_at
        )
        cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()

def get_filtered_vacancies(conn, filters):
    cursor = conn.cursor()
    query = read_sql_file('select_vacancies.sql')
    keyword = '%' + filters.get('keyword', '') + '%'
    area = '%' + filters.get('area', '') + '%'
    salary_from = filters.get('salary_from')
    salary_to = filters.get('salary_to')
    salary_from = None if salary_from == '' else salary_from
    salary_to = None if salary_to == '' else salary_to
    cursor.execute(query, (
        keyword, filters.get('keyword', ''),
        area, filters.get('area', ''),
        salary_from, salary_from,
        salary_to, salary_to
    ))
    vacancies = cursor.fetchall()
    cursor.close()
    conn.close()
    return vacancies

def get_vacancy_statistics(conn, keyword):
        cursor = conn.cursor()
        query = read_sql_file('select_vacancy_statistics.sql')
        cursor.execute(query, ('%' + keyword + '%',))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count