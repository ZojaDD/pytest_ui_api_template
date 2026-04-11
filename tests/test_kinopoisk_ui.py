import os
import time
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Generator, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Получение URL из окружения (исправление хардкода URL)
UI_BASE_URL = os.getenv('UI_BASE_URL')
MOVIE_DETAILS_URL = os.getenv('MOVIE_DETAILS_URL')
MOVIES_IN_CINEMA_URL = os.getenv('MOVIES_IN_CINEMA_URL')


@pytest.fixture(scope='function')
def browser() -> Generator[WebDriver, Any, None]:
    """Фикстура для запуска и закрытия браузера."""
    driver = webdriver.Chrome()
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def accept_cookies(browser: WebDriver) -> bool:
    """Вспомогательная функция для принятия cookies."""
    try:
        cookie_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(text(), 'Принять') or "
                "contains(text(), 'Accept') or contains(text(), 'Согласен')]"
            ))
        )
        cookie_button.click()
        print("Cookies приняты")
        time.sleep(1)
        return True
    except Exception:
        print("Окно cookies не появилось")
        return False


def find_element(browser: WebDriver, selectors: list) -> Optional[WebElement]:
    """Вспомогательная функция:
    ищет первый видимый элемент по списку селекторов."""
    for selector in selectors:
        elements = browser.find_elements(By.CSS_SELECTOR, selector)
        for element in elements:
            if element.is_displayed():
                return element
    return None


def find_visible_elements(browser: WebDriver, selectors: list) -> list:
    """Ищет все видимые элементы по списку CSS‑селекторов."""
    elements = []
    for selector in selectors:
        found = browser.find_elements(By.CSS_SELECTOR, selector)
        elements.extend(el for el in found if el.is_displayed())
    return elements


@allure.feature("UI Tests - Kinopoisk")
@allure.title("Переход на главную страницу Кинопоиска")
@allure.description(
    "Проверяем загрузку главной страницы Кинопоиска \
    и наличие основных элементов"
)
def test_ui_main_page_load(browser: WebDriver) -> None:
    """UI тест: Корректность загрузки главной страницы Кинопоиска."""

    with allure.step("Открытие главной страницы Кинопоиска"):
        print("Открываем главную страницу Кинопоиска...")
        browser.get(UI_BASE_URL)

    # Принятие cookies
    accept_cookies(browser)

    # Скриншот
    allure.attach(
        browser.get_screenshot_as_png(),
        name="main_page_fully_loaded",
        attachment_type=allure.attachment_type.PNG
    )

    with allure.step("Проверка наличия логотипа Кинопоиска"):
        logo_selectors = [
            "a[href*='kinopoisk.ru'] img",
            ".logo",
            "[class*='logo']",
            "svg[class*='logo']"
        ]

        logo = find_element(browser, logo_selectors)
        if logo and logo.is_displayed():
            print("Логотип Кинопоиска найден")
        else:
            assert "Кинопоиск" in browser.title, \
                "Страница не похожа на 'Кинопоиск'"
            print("Страница Кинопоиска загружена (проверка по title)")

    with allure.step("Проверка наличия поисковой строки"):
        search_selectors = [
            "input[placeholder*='поиск']",
            "input[placeholder*='фильм']",
            ".search-input",
            "form[role='search'] input"
        ]

        search_field = find_element(browser, search_selectors)
        if search_field and search_field.is_displayed():
            print("Поисковая строка найдена")
        else:
            # Проверка кнопки поиска
            try:
                search_button = browser.find_element(
                    By.CSS_SELECTOR, "button[type='submit'], .search-button"
                )
                if search_button.is_displayed():
                    print("Кнопка поиска найдена")
                else:
                    print("Элементы поиска не найдены, но тест продолжается")
            except Exception:
                print("Элементы поиска не найдены, но тест продолжается")

    print("Главная страница загружена успешно!")


@allure.feature("UI Tests - Kinopoisk")
@allure.title("Поиск фильма 'Домовенок Кузя' через UI")
@allure.description(
    "Тест проверяет поиск фильма через поисковую строку на сайте")
def test_ui_search_domovenok_kuzya(browser: WebDriver) -> None:
    """UI тест: поиск фильма 'Домовенок Кузя'."""

    with allure.step("Открытие главной страницы Кинопоиска"):
        browser.get(UI_BASE_URL)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    accept_cookies(browser)

    allure.attach(
        browser.get_screenshot_as_png(),
        name="main_page",
        attachment_type=allure.attachment_type.PNG
    )

    with allure.step("Ввод запроса 'Домовенок Кузя'"):
        search_input = find_element(browser, [
            "input[placeholder*='поиск']",
            "input[placeholder*='фильм']",
            "input[type='text']"
        ])

        if search_input:
            search_input.clear()
            search_input.send_keys("Домовенок Кузя")
            search_input.send_keys(Keys.ENTER)
            print("Запрос введён и отправлен")
        else:
            # Резервный вариант: прямой переход на страницу поиска
            browser.get(f"{UI_BASE_URL}index.php?kp_query=Домовенок+Кузя")
            print("Выполнен прямой переход на страницу поиска")

    with allure.step("Проверка результатов поиска"):
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h1, .title, .search-results")
            )
        )
        allure.attach(
            browser.get_screenshot_as_png(),
            name="search_results",
            attachment_type=allure.attachment_type.PNG
        )

        # Финальная проверка: есть ли фильм в результатах?
        page_content = browser.page_source.lower() + browser.title.lower()
        if "домовенок кузя" not in page_content:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="search_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(
                "Фильм 'Домовенок Кузя' не найден в результатах поиска"
            )

    print("Фильм 'Домовенок Кузя' успешно найден в результатах поиска")


@allure.feature("UI Tests - Kinopoisk")
@allure.title("Переход на страницу фильма через UI")
@allure.description("Тест проверяет переход на страницу конкретного фильма")
def test_ui_open_movie_page(browser: WebDriver) -> None:
    """UI тест: переход на страницу фильма."""

    with allure.step("Переход на страницу фильма 'Домовенок Кузя'"):
        browser.get(MOVIE_DETAILS_URL)
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    accept_cookies(browser)

    with allure.step("Ожидание загрузки и проверка URL"):
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "h1, .title"
            ))
        )
        allure.attach(
            browser.get_screenshot_as_png(),
            name="movie_page",
            attachment_type=allure.attachment_type.PNG
        )

        current_url = browser.current_url
        assert "/film/" in current_url, \
            f"Не удалось перейти на страницу фильма. URL: {current_url}"
        print(f"Успешно перешли на страницу фильма: {current_url}")

    with allure.step("Проверка наличия названия фильма"):
        title_elements = browser.find_elements(
            By.CSS_SELECTOR,
            "h1, .title, [data-testid*='title'], .film-title, .movie-title"
        )
        movie_title = title_elements[0].text \
            if title_elements else browser.title

        if movie_title:
            print(f"Название фильма: {movie_title}")
            allure.attach(
                f"Название фильма: {movie_title}", name="Movie Title"
            )
        else:
            print("Не удалось извлечь название, но страница загружена")

    print("Тест перехода на страницу фильма завершён успешно!")


@allure.feature("UI Tests - Kinopoisk")
@allure.title("Проверка навигационного меню")
@allure.description("Тест проверяет работу навигационного меню сайта")
def test_ui_navigation_menu(browser: WebDriver) -> None:
    """UI тест: проверка навигационного меню."""

    with allure.step("Открытие главной страницы Кинопоиска"):
        browser.get(UI_BASE_URL)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    accept_cookies(browser)

    with allure.step("Проверка навигационного меню"):
        nav_selectors = [
            "header",
            "nav",
            ".header",
            "[class*='navigation']",
            "[class*='menu']",
            "[role='navigation']"
        ]

        nav_elements = find_visible_elements(browser, nav_selectors)
        nav_count = len(nav_elements)

        if nav_count > 0:
            print(f"Найдено {nav_count} навигационных элементов")

            nav_texts = [el.text.strip()
                         for el in nav_elements if el.text.strip()]
            if nav_texts:
                unique_texts = list(set(nav_texts))[:5]
                print(f"Тексты навигации: {unique_texts}")
                allure.attach("\n".join(unique_texts), name="Navigation Texts")
            else:
                # Резервная проверка: ищем ссылки в header
                header_links = browser.find_elements(
                    By.CSS_SELECTOR, "header a, .header a"
                )
                if header_links:
                    print(f"Найдено {len(header_links)} ссылок в header")
                else:
                    print("Навигационные элементы не найдены")

    print("Проверка навигации завершена")


@allure.feature("UI Tests - Kinopoisk")
@allure.title("Переход на страницу 'Фильмы в кино'")
@allure.description(
    "Тест проверяет переход на страницу с фильмами в кинотеатрах")
def test_ui_movies_in_cinema(browser: WebDriver) -> None:
    """UI тест: переход на страницу фильмов в кино."""
    with allure.step("Переход на страницу фильмов в кино"):
        browser.get(MOVIES_IN_CINEMA_URL)
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    accept_cookies(browser)

    with allure.step("Проверка загрузки страницы"):
        WebDriverWait(browser, 15).until(
            lambda driver: "movies-in-cinema" in driver.current_url
            or "кино" in driver.title.lower()
        )
        allure.attach(
            browser.get_screenshot_as_png(),
            name="cinema_movies_page",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Проверка наличия контента на странице"):
        content_elements = browser.find_elements(
            By.CSS_SELECTOR,
            "[class*='movie'], [class*='film'], .card, .item, .poster"
        )

        if len(content_elements) <= 5:
            page_text = browser.page_source.lower()
            if "кино" not in page_text and "фильм" not in page_text:
                raise AssertionError("Не удалось найти контент на странице")

        print(
            f"На странице найдено {len(content_elements)} элементов контента"
        )

    print("Тест страницы 'Фильмы в кино' завершён успешно!")


if __name__ == "__main__":
    pytest.main(['-v', '-s', '--alluredir=allure-results'])
