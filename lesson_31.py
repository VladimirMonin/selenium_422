# Импорт selenium webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
# Создание экземпляра браузера
# driver = webdriver.Firefox()
driver = webdriver.Chrome()

# Переход на сайт гугла
driver.get("https://www.google.com/")

# Ищем элемент по тегу texarea
# driver.find_element_by.... УСТАРЕЛО
# НАС ИНТЕРЕСУЕТ ИНТРУМЕНТ By
search_form = driver.find_element(By.TAG_NAME, "textarea")

# Ввод поискового запроса
search_form.send_keys("Котики фото")

# Отправка поискового запроса 
search_form.submit()

# Поискать тег a с классом nPDzT 
image_button = driver.find_element(By.CSS_SELECTOR, "a.nPDzT")

# клик
image_button.click()

# Имитация прокрутки колесом мыши
for i in range(10):
    sleep(2)
    driver.execute_script("window.scrollBy(0, 1000);")


# Пауза 5 секунд
sleep(10)
driver.quit()

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
