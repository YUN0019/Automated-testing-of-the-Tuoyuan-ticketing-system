import time
import random
import base64
import os
import pickle
from PIL import Image
import pytesseract
import undetected_chromedriver as uc  # 改用 undetected_chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytesseract.pytesseract.tesseract_cmd = r'c:\Users\user\Desktop\robot\exes\tesseract.exe'

CHROME_VERSION_MAIN = 149
DEBUG_MODE = True
COOKIE_PATH = "cookies.pkl"
IMAGE_DIR = "wrongjpg"

os.makedirs(IMAGE_DIR, exist_ok=True)

def human_sleep(a=0.5, b=1.5):
    time.sleep(random.uniform(a, b))

def human_click(element):
    human_sleep()
    element.click()

def solve_captcha(driver):
    try:
        captcha_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img#captcha_image"))
        )
        captcha_src = captcha_img.get_attribute("src")

        if "data:image" in captcha_src:
            header, encoded = captcha_src.split(",", 1)
            image_data = base64.b64decode(encoded)

            captcha_path = os.path.join(IMAGE_DIR, "captcha.png")
            with open(captcha_path, "wb") as f:
                f.write(image_data)

            image = Image.open(captcha_path)
            captcha_text = pytesseract.image_to_string(
                image, config="--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

            return captcha_text.strip()
        else:
            print("\u274c \u9a57\u8b49\u78bc\u5716\u7247\u975e base64 \u683c\u5f0f")
            return ""
    except Exception as e:
        print("\u274c \u9a57\u8b49\u78bc\u89e3\u6790\u932f\u8aa4:", e)
        return ""

def save_cookies(driver, path=COOKIE_PATH):
    with open(path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print("\u2705 \u5df2\u5132\u5b58 Cookie")

def load_cookies(driver, path=COOKIE_PATH):
    try:
        with open(path, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            if 'sameSite' in cookie and cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
            driver.add_cookie(cookie)
        print("\u2705 \u5df2\u8f09\u5165 Cookie")
        return True
    except Exception as e:
        print("\u26a0 \u8f09\u5165 Cookie \u5931\u6557:", e)
        return False

def create_driver(proxy=None):
    options = uc.ChromeOptions()
    chrome_user_data_dir = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data")
    options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
    options.add_argument(r"--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")

    if proxy:
        print(f"\ud83c\udf10 \u4f7f\u7528 Proxy: {proxy}")
        options.add_argument(f'--proxy-server={proxy}')

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    ]
    ua = random.choice(user_agents)
    options.add_argument(f'--user-agent={ua}')

    try:
        driver = uc.Chrome(version_main=CHROME_VERSION_MAIN, options=options)
        print("\u2705 \u6210\u529f\u555f\u52d5 Chrome")
        return driver
    except Exception as e:
        print("\u274c \u7121\u6cd5\u555f\u52d5 Chrome\uff1a", e)
        raise

def wait_for_sell_start(driver, wait, proxy_list, current_proxy_index, check_interval=0.5, timeout=300):
    start_time = time.time()
    while True:
        try:
            if "Queue" in driver.title or "\u6392\u968a" in driver.page_source:
                print("\u23f3 \u6392\u968a\u4e2d\uff0c\u81ea\u52d5\u5237\u65b0\u7b49\u5f85...")
                driver.refresh()
                time.sleep(2)
                continue

            buy_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'\u7acb\u5373\u8a02\u8cfc')]")))
            human_click(buy_button)
            print("\u2705 \u9ede\u64ca\u300e\u7acb\u5373\u8a02\u8cfc\u300f")
            return True, current_proxy_index

        except Exception as e:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                print("\u274c \u8d85\u6642\uff0c\u5617\u8a66\u5207\u63db Proxy")
                current_proxy_index += 1
                if current_proxy_index >= len(proxy_list):
                    print("\u274c Proxy \u6e05\u55ae\u7528\u76e1")
                    return False, current_proxy_index
                driver.quit()
                driver = create_driver(proxy_list[current_proxy_index])
                driver.get("https://tixcraft.com/")
                load_cookies(driver)
                wait = WebDriverWait(driver, 10)
                start_time = time.time()
                continue
            else:
                print("\u23f3 \u7b49\u5f85\u958b\u8ce3\u4e2d...", e)
                driver.refresh()
                time.sleep(check_interval)

def is_logged_in(driver):
    try:
        driver.find_element(By.LINK_TEXT, "\u767b\u51fa")
        return True
    except:
        return False

def main():
    proxy_list = []
    current_proxy_index = 0
    driver = create_driver(proxy_list[current_proxy_index] if proxy_list else None)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://tixcraft.com/")
        time.sleep(3)

        loaded = load_cookies(driver)
        if loaded and is_logged_in(driver):
            driver.refresh()
            time.sleep(3)
            print("\u5617\u8a66\u81ea\u52d5\u767b\u5165\u4e2d...")
        else:
            print("\u8acb\u624b\u52d5\u767b\u5165\u5e33\u865f\uff0c\u5b8c\u6210\u5f8c\u6309 Enter \u7e7c\u7e8c\u4e26\u5132\u5b58 cookie...")
            input()
            if not is_logged_in(driver):
                print("\u274c \u767b\u5165\u5931\u6557\uff0c\u8acb\u91cd\u65b0\u57f7\u884c\u7a0b\u5f0f")
                driver.quit()
                return
            save_cookies(driver)
            print("\u2705 \u5df2\u5132\u5b58 cookie\uff0c\u4e0b\u6b21\u53ef\u81ea\u52d5\u767b\u5165")
            if DEBUG_MODE:
                input("\u6309 Enter \u95dc\u9589\u700f\u89bd\u5668...")
            driver.quit()
            return

        # 搶票流程照常繼續...
        # ... 此處略，因你未要求變更這部分

    except Exception as e:
        print("\u274c \u4e3b\u6d41\u7a0b\u932f\u8aa4\uff1a", e)

    finally:
        if DEBUG_MODE:
            input("\ud83d\udd52 DEBUG \u6a21\u5f0f\u958b\u555f\uff1a\u6309 Enter \u95dc\u9589\u700f\u89bd\u5668...")
        else:
            driver.quit()

if __name__ == "__main__":
    main()

