import requests
import pandas as pd
from bs4 import BeautifulSoup as Bs
from user_agent import generate_user_agent

# get the target web info using requests
headers = {}
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
              Chrome/83.0.4103.97 Safari/537.36'
cookies = '__mta=149705993.1592921749589.1592921749589.1592921749589.1; uuid_n_v=v1; \
           uuid=759EC3B0B55811EA974289B279A7041D54617AC57BFE484ABA5320834BD9EE08; _lx\
           sdk_cuid=172e1718573c8-0ff039dc6606de-1c29180f-1fa400-172e1718573c8; _lxsdk\
           =759EC3B0B55811EA974289B279A7041D54617AC57BFE484ABA5320834BD9EE08; mojo-uuid\
           =433f44e20e34865dfb54bd06987c9b75; _csrf=0eab5037afb3cad51d4db0645de1da96ab5\
           bb08ab375991b54679599bc22704b; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=159292\
           0213,1593139168; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; mojo-sessi\
           on-id={"id":"fc2b3fe958b44fdece2980b56acf7fa8","time":1593150055430}; mojo-trace\
           -id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593150187; __mta=149705993.15929\
           21749589.1592921749589.1593150186918.2; _lxsdk_s=172ef24a197-c27-2e1-d9e%7C%7C13'
headers['user-Agent'] = user_agent
headers['cookies'] = cookies
target_url = 'https://maoyan.com/films?showType=3&sortId=1'
res = requests.get(target_url, verify=False, headers=headers)
res.encoding = 'utf-8'

# test code in local machine
# url = 'E:\经典影片_电影大全_经典高清电影-猫眼电影.html'
# html = ''
# with open(url, 'r', encoding='utf-8') as fp:
#     html = fp.read()

# parser the html data of target website
ans = []
res_info = Bs(res.text, 'html.parser')
for tags in res_info.find_all('div', attrs={'class': 'movie-hover-info'}):
    my_dict = {}
    for i, tag in enumerate(tags.find_all('div', attrs={'class': 'movie-hover-title'})):
        data = tag.text.strip().split('\n')
        if not i:
            my_dict['名称'] = data[0]
        else:
            my_dict[data[0][:-1]] = data[1].strip()

    ans.append(my_dict)
    if len(ans) == 10:
        break

# save filtered data using pandas
df = pd.DataFrame(ans, columns=list(ans[0].keys()))
df.to_csv('./data.csv', index=False, encoding='GBK')
