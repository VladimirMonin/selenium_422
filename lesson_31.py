# Импорт selenium webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
# Создание экземпляра браузера
# driver = webdriver.Firefox()
driver = webdriver.Chrome()
MAIN_URL = 'https://books.toscrape.com/'
# Методы поиска элементов
# find_element - Найдет первый попавшийся элемент
# find_elements - Найдет все элементы
# By - специальный класс для выборки элементов
# By.TAG_NAME - поиск по тегу
# By.CLASS_NAME - поиск по классу
# By.CSS_SELECTOR - поиск по CSS селектору
# By.ID - поиск по атрибуту id
# By.LINK_TEXT - поиск по тексту ссылки
# By.PARTIAL_LINK_TEXT - поиск по части текста ссылки
# By.NAME - поиск по атрибуту name
# By.XPATH - поиск по XPath

# click - Вызывает событие клика по элементу
# send_keys - Вызывает событие ввода текста в элемент
# submit - Вызывает событие отправки формы

# webElement - служебный объект, который возвращается при поиске элемента

# Переход на сайт books.toscrape.com
driver.get(MAIN_URL)
sleep(1)
# Найти все элементы с классом product_pod
books = driver.find_elements(By.CLASS_NAME, "product_pod")



"""
https://books.toscrape.com/
catalogue/a-light-in-the-attic_1000/index.html

https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html

https://books.toscrape.com/
media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg

https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg

0. Полный заголовок книги атрибут title в ссылке в заголовке h3 > a['title']
1. Первый тег a href - ссылка на детальное отображение товара
2. Первый тег а img src - ссылка на обложку
3. p.price_color - цена в формате £51.77 (отрезать фунты и сделать флоат)
4. p.instock - если есть второй класс availability - доступно в продаже
5. Оценка p.star-rating нам нужен его второй класс (One Two Three Four Five) - оценка

"""

for book in books:
    # h3 - Заголовок книги
    title = book.find_element(By.TAG_NAME, "h3").text
    print(title)
    # Полный текст живет в аттрибуте title
    full_title = book.find_element(By.CSS_SELECTOR, "h3 > a").get_attribute("title")
    print(full_title)