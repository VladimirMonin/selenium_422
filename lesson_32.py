"""
Функции для сбора данных с сайта Booktoscrape.com
get_dirver - отдает экземпляр драйвера
get_product_cards - принимает драйвер, отдает WebElement КАРТОЧЕК
get_title_by_card - принимает WebElement отдает строку
get_book_url_by_card - принимает WebElement отдает строку
get_book_cover_url_by_card - принимает WebElement отдает строку
get_book_price_by_card - принимает WebElement отдает float
get_book_availability_by_card - принимает WebElement отдает bool
get_book_mark_by_card - принимает WebElement отдает int
get_book_data_by_card - агрегатор. Использует другие функции для сбора инфы
get_data_by_page - собирает все с одной страницы принимает КАРТОЧКИ и обрабатывает их get_book_data_by_card
get_page_count - принимает драйвер, отдает int
save_data_to_csv - принимает список словарей и записывает в CSV Документ
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from pprint import pprint
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import csv
# Импорт 

MAIN_URL = 'https://books.toscrape.com/'
MAKR_DICT = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

SCV_FILE = 'result.csv'

def get_dirver(headless=False) -> webdriver.Chrome:
    options = Options()
    if headless:
        # Скрытый запуск
        options.add_argument("--headless=new")
        # FHD разрешение
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)
    # Разворот на весь экран при старте
    options.add_argument("--start-maximized")
    
    return webdriver.Chrome(options=options)
    

def get_product_cards(driver: webdriver.Chrome) -> list[WebElement]:
    """
    Принимает драйвер, отдает список веб WebElement карточек
    """
    # Получаем все карточки
    cards = driver.find_elements(By.CLASS_NAME, "product_pod")
    return cards


def get_title_by_card(card: WebElement) -> str|None:
    """
    Принимает WebElement карточки, отдает строку
    """
    full_title = card.find_element(By.CSS_SELECTOR, "h3 > a").get_attribute("title")
    return full_title

def get_book_url_by_card(card: WebElement) -> str|None:
    """
    Принимает WebElement карточки, отдает строку
    """
    book_url = card.find_element(By.CSS_SELECTOR, "h3 > a").get_attribute("href")
    return book_url

def get_book_cover_url_by_card(card: WebElement) -> str | None:
    """
    Принимает WebElement карточки, отдает строку
    """
    book_cover = card.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    return book_cover


# get_book_price_by_card - принимает WebElement отдает float


def get_book_price_by_card(card: WebElement) -> float:
    """
    Принимает WebElement карточки, отдает float
    """
    book_price = float(card.find_element(By.CSS_SELECTOR, "p.price_color").text.lstrip('£'))
    return book_price

def get_book_availability_by_card(card: WebElement) -> bool:
    """
    Принимает WebElement карточки, отдает bool
    """
    # Доступность книги p.instock - если второй класс availability - доступно в продаже
    book_availability_classes = card.find_element(By.CSS_SELECTOR, "p.instock").get_attribute("class") # Вернет все классы строкой типа instock availability ....
    book_availability = True if "availability" in book_availability_classes.lower() else False

    return book_availability


def get_book_mark_by_card(card: WebElement) -> int:
    """
    Принимает WebElement карточки, отдает int
    """
    str_mark = (
        card.find_element(By.CSS_SELECTOR, "p.star-rating") # star-rating One
        .get_attribute("class")
        .split(" ")[1]
    )
    mark = MAKR_DICT[str_mark]

    return mark


# get_book_data_by_card - агрегатор. Использует другие функции для сбора инфы возвращая словарь
# full_title
# book_url
# book_cover
# book_price
# book_availability
# book_rating


def get_book_data_by_card(card: WebElement) -> dict:
    """
    Принимает WebElement карточки, отдает словарь
    """
    book_data = {
        "full_title": get_title_by_card(card),
        "book_url": get_book_url_by_card(card),
        "book_cover": get_book_cover_url_by_card(card),
        "book_price": get_book_price_by_card(card),
        "book_availability": get_book_availability_by_card(card),
        "book_rating": get_book_mark_by_card(card),
    }

    return book_data

# get_data_by_page - собирает все с одной страницы принимает КАРТОЧКИ и обрабатывает их get_book_data_by_card
def get_data_by_page(cards: list[WebElement]) -> list[dict]:
    """
    Принимает список карточек, отдает список словарей.
    Обрабатывает 1 страницу сайта
    """
    book_data = []
    for card in cards:
        book_data.append(get_book_data_by_card(card))
    return book_data



# get_page_count - принимает драйвер, отдает int  ul.pager > li.current текст.split(" ")[-1]


def get_page_count(driver: webdriver.Chrome) -> int:
    """
    Принимает драйвер, отдает int
    """
    page_count = driver.find_element(
        By.CSS_SELECTOR, "ul.pager > li.current"
    ).text.split(" ")[-1]
    return int(page_count)

# save_data_to_csv - принимает список словарей и записывает в CSV Документ


def save_data_to_csv(data: list[dict], file_name: str) -> None:
    """
    Принимает список словарей, записывает в CSV файл
    """
    with open(file_name, "a", encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(
            file, fieldnames=data[0].keys(), lineterminator="\n", delimiter=";"
        )
        for row in data:
            try:
                writer.writerow({k: v.encode('utf-8').decode('utf-8') if isinstance(v, str) else v for k, v in row.items()})
            except UnicodeEncodeError:
                writer.writerow({k: v.encode('utf-8', 'ignore').decode('utf-8') if isinstance(v, str) else v for k, v in row.items()})


def main():
    
    # Получаем Driver
    driver = get_dirver(headless=False)
    
    # Переходим на сайт
    driver.get(MAIN_URL)
    sleep(1)
    
    # Получаем количество страниц
    page_count = get_page_count(driver)
    print(f"Количество страниц {page_count}")
    
    # Цикл по страницам сайта
    for page_num in range(1, page_count + 1):
        print(f"Парсинг страницы {page_num} из {page_count}")
        
        # Получаем список WebElements карточек
        cards = get_product_cards(driver)

        # Получаем список словарей
        book_data = get_data_by_page(cards)
        
        # Сохраняем данные
        save_data_to_csv(book_data, SCV_FILE)
        
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, "ul.pager > li.next > a")
        
        except:
            print("Страницы закончились")
            break
        
        else:
            next_page.click()
        
        # Сон для загрузки страницы
        sleep(1)
    
    driver.close()


if __name__ == "__main__":
    main()
