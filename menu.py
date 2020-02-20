# coding=utf-8
from urllib.request import Request, urlopen, urlretrieve, build_opener, install_opener
from urllib.parse import urlencode
from os.path import exists
from os import mkdir
import codecs
from warnings import simplefilter
simplefilter('ignore', DeprecationWarning)

#global variables
url = "http://www.kebuke.com/"
values = {"_Page": "index", "mode": "info", "_lang": "T"}
# set headers
headers = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")]
opener = build_opener()
opener.addheaders = headers
install_opener(opener)


def get_desc(store):
    """get store name, picture, description \n
    return str"""
    global url, values
    values["store"] = store  # 輸入店號
    data = urlencode(values).encode("big5")  # 將data轉成bytes
    request = Request(url, data=data)  # 製作request
    response = urlopen(request)  # 接收response
    html = response.read()
    return codecs.decode(html, "unicode_escape")  # 解碼

#title, pic, desc


def text_to_str(text):
    """turning text to csv_form str\n
    return str"""
    text = text.replace('\n', '').replace('\r', '')  # important!! \r
    i1 = text[10:].find('店"') + 11
    i2 = i1 + text[i1:].find('"http') + 1
    i3 = i2 + text[i2:].find('g","desc"') + 1
    i4 = i3 + text[i3:].find('desc":"') + 7
    t = text[10:i1] + "," + text[i2:i3].replace("\\", "") + "," + text[i4:-2]

    return t


def get_all_descriptions(fname):
    # send requests to get store description
    stores = []
    for store in range(200):  # store id < 200
        text = get_desc(store)
        if text[:30].find("title") != -1 and text[:30].find("店") != -1:
            stores.append(text_to_str(text))

    # write store description
    with open(fname, 'w', encoding='utf8') as f:
        f.write("\n".join(stores))


def read_stores(fname):
    """read in text.csv \n
    return a list of str"""
    with open(fname, 'r', encoding="utf8") as f:
        stores = [x.split(',') for x in f.readlines()]

    return stores


def download_pic(store, path):
    urlretrieve(store[1], path + '/' + store[0] + store[1][-4:])


def download_all_pictures(path):
    if not exists(path):
        mkdir(path)
    for store in stores:
        download_pic(store, path)


if __name__ == "__main__":
    print("get_all_descriptions")
    get_all_descriptions("./text.csv")

    print("read_stores")
    stores = read_stores("./text.csv")

    print("download_all_pictures")
    download_all_pictures("./card")

    print("finished")
