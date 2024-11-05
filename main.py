from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from telegram import Bot
from datetime import datetime
import logging

# Установим уровень логирования для вывода информации
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь для сохранения скриншотов
base_output_dir = r"C:\Users\ridzi\OneDrive\Рабочий стол\кцэт\тестирование\algoritmika\test3"

# Создание папки с текущей датой и временем
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_dir = os.path.join(base_output_dir, current_time)
os.makedirs(output_dir, exist_ok=True)

# Настройки для запуска Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.binary_location = r"C:\Users\ridzi\Downloads\chrome-win64\chrome.exe"  # Убедитесь, что путь корректен

# Запуск браузера с Selenium
try:
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://algoritmika.org/ru")
except Exception as e:
    logging.error(f"Ошибка при запуске браузера: {e}")
    raise  # Остановить выполнение, если браузер не запускается

wait = WebDriverWait(driver, 10)

# Настройки Telegram
TELEGRAM_TOKEN = 'user_token'
CHAT_ID = 'user_ID'

# Функция для отправки сообщения и фото в Telegram
def send_message_with_photo(bot, chat_id, message, photo_path):
    logging.info(f"Отправка сообщения в Telegram: {message}")
    bot.send_message(chat_id=chat_id, text=message)
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)
    logging.info("Сообщение и фото успешно отправлены в Telegram.")

# Инициализация бота Telegram
bot = Bot(token=TELEGRAM_TOKEN)

# Тестируемые элементы
elements = {
    "logo": (By.CSS_SELECTOR, ".header__logo"),
    "logo_text": (By.CSS_SELECTOR, ".header__logo-text"),
    "login_button": (By.CSS_SELECTOR, ".login-button"),
    "active_nav_item": (By.CSS_SELECTOR, ".header__navigation-item a[data-v-6c994a70]")
}

# Проверка элементов и отправка отчетов
results = {}
for name, locator in elements.items():
    try:
        # Ожидание элемента и его видимости
        element = wait.until(EC.visibility_of_element_located(locator))
        screenshot_path = os.path.join(output_dir, f"{name}_{current_time}.png")
        element.screenshot(screenshot_path)
        timestamped_message = f"[{current_time}] Элемент '{name}' найден, скриншот сохранен: {screenshot_path}"
        results[name] = timestamped_message

        # Отправка результата и скриншота в Telegram
        send_message_with_photo(bot, CHAT_ID, timestamped_message, screenshot_path)
        print(timestamped_message)

    except Exception as e:
        timestamped_error = f"[{current_time}] Элемент '{name}' не найден. Ошибка: {str(e)}"
        results[name] = timestamped_error
        logging.error(f"Ошибка при проверке элемента {name}: {e}")

        # Отправка сообщения об ошибке в Telegram
        bot.send_message(chat_id=CHAT_ID, text=timestamped_error)
        print(timestamped_error)

# Закрытие браузера
driver.quit()

# Итоговый вывод результатов в консоль
logging.info("Результаты тестирования:")
for element_name, result in results.items():
    print(f"{element_name}: {result}")









