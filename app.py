from flask import Flask, render_template
from dotenv import load_dotenv
import os
from routes import configure_routes
from database import connect_to_db, db_params

# Загрузка переменных окружения из файла .env
load_dotenv()

app = Flask(__name__)

# Настройка маршрутов
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)