import time
import pyautogui
from selenium import webdriver

login_url = "https://shimo.im/login?from=home"


def get_username():
    return pyautogui.prompt(text="Please input phone num/email", title="User name", default="", )


def get_password():
    return pyautogui.password(text="Please input your password", title="Password", default="", mask="*")


if __name__ == '__main__':
    user_name = get_username()
    password = get_password()

    try:
        browser = webdriver.Firefox()
        browser.get(login_url)
        time.sleep(5)

        browser.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys(user_name)
        time.sleep(1)
        browser.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys(password)
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()
        time.sleep(1)

        cookies = browser.get_cookies()  # 获取cookies
        print(cookies)
        time.sleep(3)

    except Exception as e:
        print(e)
    finally:
        browser.close()
