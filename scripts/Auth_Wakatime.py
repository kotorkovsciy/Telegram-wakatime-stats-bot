from selenium.webdriver import ChromeOptions, Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from datetime import datetime as dt


async def browsedriver():
    """Драйвер для просмотра страницы"""
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.javascript": 2}
    )
    driver = Chrome(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
        chrome_options=chrome_options,
    )
    return driver


async def acc_verify(email, password):
    """Проверка аккаунта"""
    driver = await browsedriver()
    driver.get("https://wakatime.com/login")
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] acc_verify: открыт сайт')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
    )
    getEmail = driver.find_element(By.XPATH, '//*[@id="email"]')
    getEmail.send_keys(email)
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] acc_verify: введена почта')
    getPassword = driver.find_element(By.XPATH, '//*[@id="password"]')
    getPassword.send_keys(password)
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] acc_verify: введён пароль')
    button = driver.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/form/div[3]/div/button",
    )
    button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div"))
    )
    try:
        driver.find_element(By.XPATH, '//*[@id="project-title"]/b')
        print(
            f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] acc_verify: произведена авторизация'
        )
        driver.quit()
        return True
    except NoSuchElementException:
        print(
            f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] acc_verify: не произведена авторизация'
        )
        driver.quit()
        return False


async def sign_up(url, email, password):
    """Авторизация на сайте"""
    driver = await browsedriver()
    driver.get(url)
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] sign_up: открыт сайт')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
    )
    getEmail = driver.find_element(By.XPATH, '//*[@id="email"]')
    getEmail.send_keys(email)
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] sign_up: введена почта')
    getPassword = driver.find_element(By.XPATH, '//*[@id="password"]')
    getPassword.send_keys(password)
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] sign_up: введён пароль')
    button = driver.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div/div[2]/div/div/div[3]/div/form/div[3]/div/button",
    )
    button.click()
    print(
        f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] sign_up: произведена авторизация'
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div"))
    )
    try:
        button = driver.find_element(
            By.XPATH, '//*[@id="main-content"]/div/div/div/div[3]/div[2]/form/button'
        )
        button.click()
        print(
            f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] sign_up: произведено подтверждение о использовании'
        )
    except NoSuchElementException:
        pass
    finally:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[1]/p/span")
            )
        )
        code = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/p/span")
        print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] sign_up: получен код')
        code = code.get_attribute("innerHTML")
        driver.quit()
        return code
