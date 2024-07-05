from flask import Flask, request, render_template
import requests
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Параметры подключения к базе данных
db_params = {
    'dbname': 'ilvina',
    'user': 'postgres',
    'password': 'lo11p0p',
    'host': 'localhost'
}

# Функция для подключения к базе данных
def connect_to_db(params=db_params):
    conn = psycopg2.connect(**params)
    return conn

# Функция для парсинга вакансий
def parse_vacancies():
    url = 'https://api.hh.ru/vacancies'
    response = requests.get(url)
    vacancies = response.json().get('items', [])
    return vacancies

# Функция для сохранения вакансий в базу данных
def save_vacancies_to_db(conn, vacancies):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS vacancies;")
    cursor.execute("""
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            area_name VARCHAR(255),
            salary_currency VARCHAR(3),
            salary_from INTEGER,
            salary_to INTEGER,
            employer_name VARCHAR(255),
            employer_id INTEGER,
            snippet_requirement TEXT,
            snippet_responsibility TEXT,
            created_at DATE,
            published_at DATE
        );
    """)
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
        cursor.execute(
            """
            INSERT INTO vacancies (
                name, area_name, salary_currency, salary_from, salary_to,
                employer_name, employer_id, snippet_requirement,
                snippet_responsibility, created_at, published_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, data
        )
    conn.commit()
    cursor.close()

def get_vacancies_statistics(conn, keyword):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM vacancies
        WHERE name ILIKE %s;
    """, ('%' + keyword + '%',))
    count = cursor.fetchone()[0]
    cursor.close()
    return count

@app.route('/api/search', methods=['POST', 'GET'])
def search_vacancies():
    response = {'vacancies': []}
    if request.method == 'POST':
        filters = request.form
        print(f"Received filters: {filters}")
        conn = connect_to_db(db_params)
        filtered_vacancies = get_filtered_vacancies(conn, filters)
        conn.close()
        response['vacancies'] = filtered_vacancies
        print(filtered_vacancies)  
    return render_template('index.html', response=response)

def get_filtered_vacancies(conn, filters):
    cursor = conn.cursor()
    query = """
        SELECT * FROM vacancies
        WHERE (name ILIKE %s OR %s = '')
          AND (area_name ILIKE %s OR %s = '')
          AND (salary_from >= %s OR %s IS NULL)
          AND (salary_to <= %s OR %s IS NULL);
    """
    
    keyword = '%' + filters.get('keyword', '') + '%'
    area = '%' + filters.get('area', '') + '%'
    salary_from = filters.get('salary_from')
    salary_to = filters.get('salary_to')
    
    # Преобразование пустых строк в None для числовых значений
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
    return vacancies

if __name__ == '__main__':
    app.run(debug=True)