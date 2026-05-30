# Импорт основных компонентов Flask для работы с приложением, шаблонами и отправкой файлов
from flask import Flask, render_template, send_from_directory
# Импорт инструмента для управления миграциями БД
from flask_migrate import Migrate
# Импорт класса исключения для перехвата ошибок базы данных
from sqlalchemy.exc import SQLAlchemyError
# Импорт объекта БД и моделей таблиц
from models import db, Category, Image
# Импорт blueprint авторизации и функции инициализации системы логина
from auth import bp as auth_bp, init_login_manager
# Импорт blueprint курсов
from courses import bp as courses_bp

# Создание экземпляра Flask приложения
app = Flask(__name__)
# Альтернативное имя приложения для WSGI серверов
application = app

# Загрузка конфигурации из файла config.py
app.config.from_pyfile('config.py')

# Инициализация объекта БД с приложением
db.init_app(app)
# Инициализация системы миграций для приложения
migrate = Migrate(app, db)

# Инициализация менеджера авторизации пользователей
init_login_manager(app)

# Декоратор для обработки ошибок SQLAlchemy
@app.errorhandler(SQLAlchemyError)
# Функция обработчик ошибок БД
def handle_sqlalchemy_error(err):
    # Формирование дружественного сообщения об ошибке
    error_msg = ('Возникла ошибка при подключении к базе данных. '
                 'Повторите попытку позже.')
    # Возврат ошибки с кодом 500 (внутренняя ошибка сервера)
    return f'{error_msg} (Подробнее: {err})', 500

# Регистрация blueprint авторизации в приложении
app.register_blueprint(auth_bp)
# Регистрация blueprint курсов в приложении
app.register_blueprint(courses_bp)

# Маршрут для главной страницы
@app.route('/')
# Функция-обработчик для главной страницы
def index():
    # Получение всех категорий из БД
    categories = db.session.execute(db.select(Category)).scalars()
    # Отрисовка шаблона index.html с передачей списка категорий
    return render_template(
        'index.html',
        categories=categories,
    )

# Маршрут для получения изображения по ID
@app.route('/images/<image_id>')
# Функция-обработчик для отправки изображений
def image(image_id):
    # Поиск изображения в БД, при неудаче возвращает 404
    img = db.get_or_404(Image, image_id)
    # Отправка файла изображения браузеру из папки загрузок
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)
