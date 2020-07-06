import pyautogui
import requests
import time

login_url = "https://shimo.im/lizard-api/auth/password/login"
profile_url = "https://shimo.im/profile"

headers_login = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
    'Referer': 'https://shimo.im/login',
    'x-requested-with': 'XmlHttpRequest'
}

check_headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
    'authority': "shimo.im",
    'cache-control': "no-cache",
    'x-requested-with': "XmlHttpRequest",
    'x-push-client-id': "f21f404c-61dd-49fb-8061-1d733c5dd8b8",
    'scheme': "https",
    'accept': "application/vnd.shimo.v2+json",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
    'referer': "https://shimo.im/profile",
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin"
}


def get_username():
    return pyautogui.prompt(text="Please input phone num/email", title="User name", default="", )


def get_password():
    return pyautogui.password(text="Please input your password", title="Password", default="", mask="*")


def login():
    sess = requests.session()
    user_name = get_username()
    password = get_password()
    data = {
        "mobile": "+86{}".format(user_name),
        "password": "{}".format(password)
    }
    res_login = sess.post(login_url, data=data, headers=headers_login)
    print("Login status: ", res_login.status_code)
    time.sleep(5)

    res_profile = sess.get(profile_url, headers=check_headers, cookies=res_login.cookies)
    print("Check status: ", res_profile.status_code)


if __name__ == '__main__':
    login()
