import pytest
import requests
import os
import allure
from dotenv import load_dotenv

load_dotenv()

# Получение API ключа
API_KEY = os.getenv('KINOPOISK_API_KEY', '1HVYC9T-QN1MV84-H5Y1BJR-80AR0XZ')
BASE_URL = "https://api.kinopoisk.dev/"


@pytest.fixture(scope='session')
def api_client():
    """Фикстура для API клиента"""
    session = requests.Session()
    session.headers.update({
        "X-API-KEY": API_KEY,
        "accept": "application/json"
    })
    return session


@allure.feature("API Tests")
@allure.title("Проверка валидности API ключа")
@allure.description(
    "Тест проверяет, что API ключ действителен и можно получить данные")
def test_api_key_valid(api_client):
    """Тест проверки валидности API ключа"""
    with allure.step("Отправка запроса для проверки API ключа"):
        response = api_client.get(
            f"{BASE_URL}v1.4/movie",
            params={"limit": 1}
        )

    allure.attach(
        f"Status Code: {response.status_code}",
        name="Response Status",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        f"Response: {response.text[:200]}...",
        name="Response Preview")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}...")

    with allure.step("Проверка статус кода и структуры ответа"):
        assert response.status_code == 200, (
            f"API вернул статус {response.status_code}"
        )
        assert "docs" in response.json(), \
            "Ответ не содержит ключ 'docs'"

    print("API ключ валиден!")
    allure.attach("API ключ валиден!", name="Result")


@allure.feature("API Tests")
@allure.title("Поиск фильма 'Домовенок Кузя'")
@allure.description("Проверяем поиск фильма по названию")
def test_api_search_house_domovenok_kuzya(api_client):
    """Тест поиска Домовенка Кузи через API"""
    with allure.step("Выполнение поиска 'Домовенок Кузя'"):
        print("Ищем фильм по названию 'Домовенок Кузя...'")

        response = api_client.get(
            f"{BASE_URL}v1.4/movie/search",
            params={"query": "Домовенок Кузя", "limit": 3},
            timeout=10
        )

        allure.attach(
            f"Status: {response.status_code}",
            name="Search Status"
        )
        print(f"Status: {response.status_code}")

        assert response.status_code == 200, \
            f"Ошибка поиска: {response.status_code}"

        try:
            movies = response.json().get('docs', [])
        except ValueError:
            pytest.fail("Ответ не является валидным JSON")

        assert len(movies) > 0, "Фильм 'Домовенок Кузя' не найден"

        search_term = "домовенок кузя"
        found_movie = next(
            (m for m in movies if search_term in m.get('name', '').lower()),
            None
        )

        assert found_movie, "Не найден фильм 'Домовенок Кузя' в результатах"
        print(f"Найден: {found_movie['name']} "
              f"({found_movie.get('year', 'N/A')})")
        allure.attach(
            f"Найденный фильм: {found_movie['name']} "
            f"({found_movie.get('year', 'N/A')})",
            name="Found Movie"
        )


@allure.feature("API Tests")
@allure.title("Поиск высокорейтинговых фильмов")
@allure.description("Тест проверяет поиск фильмов с рейтингом 8+")
def test_api_high_rated_movies(api_client):
    """Тест высокорейтинговых фильмов через API"""
    with allure.step("Поиск фильмов с высоким рейтингом"):
        print("Ищем фильмы с высоким рейтингом...")

        response = api_client.get(
            f"{BASE_URL}v1.4/movie",
            params={
                "rating.kp": "8-10",
                "sortField": "rating.kp",
                "sortType": "-1",
                "limit": 5
            }
        )

    with allure.step("Проверка успешности запроса"):
        assert response.status_code == 200

    data = response.json()
    movies = data.get('docs', [])

    with allure.step("Проверка наличия результатов"):
        assert len(movies) > 0, "Не найдено фильмов с высоким рейтингом"

    # Проверка рейтинга
    movie_ratings = []
    for movie in movies:
        rating = movie.get('rating', {}).get('kp', 0)
        movie_ratings.append(f"{movie.get('name')}: {rating}")
        with allure.step(f"Проверка рейтинга фильма {movie.get('name')}"):
            assert rating >= 8.0, f"Фильм {movie.get('name')
                                           } имеет рейтинг {rating} < 8.0"

    allure.attach("\n".join(movie_ratings), name="Movies with ratings ≥ 8.0")
    print(f"Найдено {len(movies)} фильмов с рейтингом ≥ 8.0")


@allure.feature("API Tests")
@allure.title("Поиск фильмов по году")
@allure.description("Проверяем поиск фильмов 2025 года")
def test_api_movies_by_year(api_client):
    """Тест фильмов по году через API"""
    with allure.step("Поиск фильмов 2025 года"):
        print("Ищем фильмы 2025 года...")

        response = api_client.get(
            f"{BASE_URL}v1.4/movie",
            params={"year": "2025", "limit": 5}
        )

    with allure.step("Проверка успешности запроса"):
        assert response.status_code == 200

    data = response.json()
    movies = data.get('docs', [])

    with allure.step("Проверка наличия результатов"):
        assert len(movies) > 0, "Не найдено фильмов 2025 года"

    # Проверка - год выпуска фильма
    movie_list = []
    for movie in movies:
        movie_list.append(f"{movie.get('name')} ({movie.get('year')})")
        with allure.step(f"Проверка года выпуска {movie.get('name')}"):
            assert movie.get(
                'year') == 2025, f"Фильм {movie.get('name')} не 2025 года"

    allure.attach("\n".join(movie_list), name="Movies from 2025")
    print(f"Найдено {len(movies)} фильмов 2025 года")


@allure.feature("API Tests")
@allure.title("Негативный тест: поиск фильма из 1870 года")
@allure.description(
    "Проверяем, что API возвращает ошибку 400 \
    при поиске фильмов из несуществующего периода (1870 год)")
def test_api_search_movie_1870_year(api_client):
    """Негативный тест поиска фильма 1870 года через API"""
    with allure.step("Выполнение поиска фильмов 1870 года"):
        print("Ищем фильмы 1870 года (ожидаем ошибку 400)...")

        response = api_client.get(
            f"{BASE_URL}v1.4/movie",
            params={"year": "1870", "limit": 5}
        )

    allure.attach(
        f"Status Code: {response.status_code}",
        name="Response Status"
    )
    allure.attach(
        f"Response: {response.text[:200]}...",
        name="Response Preview"
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}...")

    with allure.step("Проверка статус‑кода ошибки"):
        assert response.status_code == 400, (
            f"Ожидался статус 400 (Bad Request), \
            но получен {response.status_code}. "
            "Это может означать, что API не валидирует год \
            или обрабатывает запрос иначе."
        )

    try:
        error_data = response.json()
        allure.attach(
            str(error_data),
            name="Error Response JSON"
        )

        # Дополнительная проверка структуры ошибки
        with allure.step("Проверка структуры ответа об ошибке"):
            # Проверяем наличие ключевых полей
            assert "error" in error_data or "message" in error_data, (
                "Ответ об ошибке не содержит ожидаемых полей \
                'error' или 'message'"
            )

    except ValueError:
        # Если ответ не в формате JSON
        allure.attach(
            response.text,
            name="Error Response (non‑JSON)"
        )
        print("Предупреждение: ответ об ошибке не в формате JSON")

    print("Тест пройден: "
          "API корректно возвращает статус 400 для несуществующего года")


@allure.feature("API Tests")
@allure.title("Получение детальной информации о фильме")
@allure.description("Проверяем получение детальной информации по ID фильма")
def test_api_movie_details(api_client):
    """Тест детальной информации о фильме"""
    with allure.step("Получение детальной информации о фильме"):
        print("Получаем детальную информацию о фильме...")

        # Используем известный ID фильма
        response = api_client.get(
            f"{BASE_URL}v1.4/movie/5304528")

    with allure.step("Проверка успешности запроса"):
        assert response.status_code == 200

    movie_data = response.json()

    # Проверка - основные поля фильма
    with allure.step("Проверка основных полей фильма"):
        assert movie_data.get('name') == "Домовенок Кузя"
        assert movie_data.get('year') == 2024
        assert movie_data.get('rating', {}).get('kp') >= 6.0

    allure.attach(
        f"Название: {movie_data.get('name')}",
        name="Movie Details"
    )
    allure.attach(
        f"Год: {movie_data.get('year')}",
        name="Movie Details"
    )
    allure.attach(
        f"Рейтинг: {movie_data.get('rating', {}).get('kp')}",
        name="Movie Details"
    )

    print(f"Детали: {movie_data['name']} ({movie_data['year']})")


if __name__ == "__main__":
    pytest.main(['-v', '-s', '--alluredir=allure-results'])
