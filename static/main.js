// Использование строгого режима для более безопасного кода
'use strict';

// Обработчик для предпросмотра фоновой картинки при загрузке файла
function imagePreviewHandler(event) {
    // Проверка, загружен ли файл
    if (event.target.files && event.target.files[0]) {
        // Создание объекта для чтения файла
        let reader = new FileReader();
        // Функция, которая вызывается после загрузки файла
        reader.onload = function (e) {
            // Получение элемента изображения
            let img = document.querySelector('.background-preview > img');
            // Установка источника изображения на загруженный файл
            img.src = e.target.result;
            // Если изображение скрыто, показываем его и прячем заглушку
            if (img.classList.contains('d-none')) {
                let label = document.querySelector('.background-preview > label');
                label.classList.add('d-none');
                img.classList.remove('d-none');
            }
        }
        // Чтение файла как Data URL
        reader.readAsDataURL(event.target.files[0]);
    }
}

// Обработчик для открытия страницы курса при клике на карточку
function openLink(event) {
    // Получение ближайшей строки (row) от кликнутого элемента
    let row = event.target.closest('.row');
    // Проверка наличия URL в атрибуте data-url и переход по нему
    if (row.dataset.url) {
        window.location = row.dataset.url;
    }
}

// Инициализация обработчиков при загрузке страницы
window.onload = function() {
    // Поиск поля загрузки фонового изображения
    let background_img_field = document.getElementById('background_img');
    // Если поле найдено, привязываем обработчик
    if (background_img_field) {
        background_img_field.onchange = imagePreviewHandler;
    }
    // Для каждой карточки курса добавляем обработчик клика
    for (let course_elm of document.querySelectorAll('.courses-list .row')) {
        course_elm.onclick = openLink;
    }
}