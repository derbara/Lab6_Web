# Импорт компонентов Flask для создания модуля, шаблонов, перенаправлений и флеш-сообщений
from flask import Blueprint, render_template, redirect, url_for, flash, request
# Импорт компонентов Flask-Login для управления авторизацией пользователей
from flask_login import LoginManager, login_user, logout_user, login_required
# Импорт объекта БД и модели пользователя
from models import db, User

# Создание blueprint модуля авторизации с префиксом /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Функция инициализации менеджера авторизации
def init_login_manager(app):
    # Создание экземпляра менеджера логина
    login_manager = LoginManager()
    # Установка маршрута для перенаправления неавторизованных пользователей
    login_manager.login_view = 'auth.login'
    # Сообщение, которое показывается при попытке доступа без авторизации
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    # Категория флеш-сообщения (для стилизации)
    login_manager.login_message_category = 'warning'
    # Регистрация функции загрузки пользователя по ID
    login_manager.user_loader(load_user)
    # Инициализация менеджера с приложением
    login_manager.init_app(app)

# Функция для загрузки пользователя из БД по ID
def load_user(user_id):
    # Поиск пользователя в БД по ID
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    # Возврат объекта пользователя
    return user

# Маршрут для входа в систему (поддерживает GET и POST запросы)
@bp.route('/login', methods=['GET', 'POST'])
# Функция-обработчик входа
def login():
    # Проверка, является ли запрос POST (отправка формы)
    if request.method == 'POST':
        # Получение логина из формы
        login = request.form.get('login')
        # Получение пароля из формы
        password = request.form.get('password')
        # Проверка, что оба поля заполнены
        if login and password:
            # Поиск пользователя в БД по логину
            user = db.session.execute(db.select(User).filter_by(login=login)).scalar()
            # Проверка, существует ли пользователь и верный ли пароль
            if user and user.check_password(password):
                # Авторизация пользователя в системе
                login_user(user)
                # Успешное флеш-сообщение
                flash('Вы успешно аутентифицированы.', 'success')
                # Получение URL страницы, на которую пользователь хотел перейти
                next = request.args.get('next')
                # Перенаправление на запрошенную страницу или на главную
                return redirect(next or url_for('index'))
        # Сообщение об ошибке при неверных учетных данных
        flash('Введены неверные логин и/или пароль.', 'danger')
    # Отрисовка шаблона формы входа
    return render_template('auth/login.html')

# Маршрут для выхода из системы
@bp.route('/logout')
# Декоратор, требующий авторизацию для доступа
@login_required
# Функция-обработчик выхода
def logout():
    # Удаление сессии текущего пользователя
    logout_user()
    # Перенаправление на главную страницу
    return redirect(url_for('index'))
