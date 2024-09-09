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
