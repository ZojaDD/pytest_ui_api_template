# pytest_ui_api_template
# Дипломный проект - тестирование сайта Кинопоиск
Цель проекта: Тестирования сайта КиноПоиск (https://www.kinopoisk.ru/) с использованием 
автоматизации UI и API, Python, Pytest, Selenium и Allure.

Проект содержит 5 UI и 5 API автотестов для веб-приложения Кинопоиск.

## Особенности реализации
**Кросс-браузерная совместимость**: Настройки Chrome оптимизированы для обхода детекции автоматизации (из-за специфики защиты сайта 
                                    необходимо проходить проверки на капчу вручную)
- **Обработка cookies**: Автоматическое принятие cookie-уведомлений
- **Гибкие селекторы**: Использование множественных селекторов для устойчивости к изменениям в верстке
- **Allure-отчеты**: Детальная документация каждого шага тестирования со скриншотами
- **Интеграция с Kinopoisk API**: Полное покрытие основных эндпоинтов API

## Шаблон для автоматизации тестирования на python

### Шаги
1. Склонировать проект 'git clone https://github.com/имя_пользователя/
   pytest_ui_api_template.git'
2. Установить зависимости
3. Запустить тесты 'pytest'

### Библиотеки (!)
- pyp install pytest
- pip install selenium
- pip install webdriver-manager
- pip install allure-pytest

### Стек:
- pytest
- selenium
- requests
- allure
- config

### Структура:
```
pytest_ui_api_template/
├── tests/
│   ├── Kinopoisk_test_ui.py          # UI-тесты для веб-интерфейса Кинопоиска
│   └── Kinopoisk_test_api.py         # API-тесты для Kinopoisk API
├── .env                    # Файл с переменными окружения и настройками
├── requirements.txt        # Зависимости проекта
└── README.md               # Документация проекта
```

### Установка и настройка

1. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Настройка переменных окружения**:
   Создать файл `.env` и настроить параметры:
   ```
   # Базовые настройки
   BASE_URL=https://www.kinopoisk.ru/
   TIMEOUT=30

   # API ключ для Kinopoisk API
   KINOPOISK_API_KEY=
   ```

## Запуск тестов

**Запуск всех тестов**:
```bash
pytest tests/ --alluredir=allure-results
```

**Запуск только UI-тестов**:
```bash
pytest tests/Kinopoisk_test_ui.py --alluredir=allure-results
```

**Запуск только API-тестов**:
```bash
pytest tests/Kinopoisk_test_api.py --alluredir=allure-results
```

**Просмотр отчета Allure**:
```bash
allure serve allure-results
```

## Охват тестирования

### UI-тесты (Diplom_test_ui.py):

- **test_ui_main_page_load** - Проверка загрузки главной страницы Кинопоиска и основных элементов
- **test_ui_search_green_mile** - Тестирование поиска фильма "Домовенок Кузя" через интерфейс
- **test_ui_open_movie_page** - Проверка перехода на страницу конкретного фильма
- **test_ui_navigation_menu** - Тестирование навигационного меню сайта
- **test_ui_movies_in_cinema** - Проверка перехода на страницу "Фильмы в кино"

### API-тесты (Diplom_test_api.py):

- **test_api_key_valid** - Проверка валидности API ключа
- **test_api_search_green_mile** - Поиск фильма "Домовенок Кузя" через API
- **test_api_high_rated_movies** - Поиск фильмов с высоким рейтингом (8+)
- **test_api_movies_by_year** - Поиск фильмов по году выпуска
- **test_api_search_movie_1870_year** - Поиск фильма из 1870 года - негативный тест
- **test_api_movie_details** - Получение детальной информации о фильме

## Автор проекта

Дипломная работа выполнена Дробязько З. Д.  Группа QA 115.2. SkyPro

**Год**: 2026