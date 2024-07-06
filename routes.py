from flask import request, render_template
from database import connect_to_db, db_params
from services import parse_vacancies, save_vacancies_to_db, get_filtered_vacancies, get_vacancy_statistics
import requests

def configure_routes(app):
    @app.route('/api/search', methods=['POST', 'GET'])
    def search_vacancies():
        response = {'vacancies': []}
        conn = connect_to_db(db_params)
        if request.method == 'POST':
            vacancies = parse_vacancies()
            save_vacancies_to_db(conn, vacancies)
            filters = request.form
            filtered_vacancies = get_filtered_vacancies(conn, filters)
            response['vacancies'] = filtered_vacancies
        else:
            cursor = conn.cursor()
            vacancies = parse_vacancies()
            save_vacancies_to_db(conn, vacancies)
            cursor.execute("SELECT * FROM vacancies")
            response['vacancies'] = cursor.fetchall()
            cursor.close()
        conn.close()
        return render_template('index.html', response=response)

    @app.route('/check_vacancies')
    def check_vacancies():
        conn = connect_to_db(db_params)
        cursor = conn.cursor()
        vacancies = parse_vacancies()
        save_vacancies_to_db(conn, vacancies)
        cursor.execute("SELECT * FROM vacancies")
        vacancies = cursor.fetchall()
        deleted_vacancies = []
        for vacancy in vacancies:
            response = requests.get(f"https://api.hh.ru/vacancies/{vacancy[7]}")
            if response.status_code == 200:
                vacancy_info = response.json()
                if vacancy_info.get('archived', False):
                    cursor.execute("DELETE FROM vacancies WHERE id = %s", (vacancy[0],))
                    deleted_vacancies.append(vacancy[1])
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('check_vacancies.html', vacancies=vacancies)
    
    @app.route('/analytics', methods=['GET'])
    def analytics():
        conn = connect_to_db(db_params)
        vacancies = parse_vacancies()
        save_vacancies_to_db(conn, vacancies)
        keyword = request.args.get('keyword', '')
        conn = connect_to_db(db_params)
        cursor = conn.cursor()
        count = get_vacancy_statistics(conn, keyword)
        cursor.close()
        conn.close()
        return render_template('analytics.html', keyword=keyword, count=count)