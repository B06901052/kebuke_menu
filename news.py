from urllib.request import Request, urlopen, urlretrieve, build_opener, install_opener
from bs4 import BeautifulSoup
import requests
import os

headers = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")]
url = "http://www.kebuke.com/"
opener = build_opener()
opener.addheaders = headers
install_opener(opener)

save_path1 = "./news1/"
save_path2 = "./news2/"
if not os.path.exists(save_path1):
    os.mkdir(save_path1)
if not os.path.exists(save_path2):
    os.mkdir(save_path2)


def get_imgs():
    global url
    re = requests.get(url)
    soup = BeautifulSoup(re.text, "lxml")
    return soup.find_all("img")


def loop(imgs):
    global url
    if os.path.exists("./error1.txt"):
        os.remove("./error1.txt")
    if os.path.exists("./error2.txt"):
        os.remove("./error2.txt")
    for img in imgs:
        img_src = img.get("src")
        if img_src[-4:] in [".jpg", '.gif', 'png'] and img_src.find("/news/") != -1:
            download(img_src)


def download(img_src):
    global url, save_path1, save_path2

    iname1 = img_src[img_src.find("/news/")+6:]
    iname2 = img_src[img_src.find("/news/")+6:-4] + "-b"
    img_url1 = url + img_src
    img_url2 = url + img_src[:-4] + "-b"
    try:
        urlretrieve(img_url1, save_path1 + iname1)
    except:
        with open("./error2.txt", 'a') as f:
            f.write(img_src+"\n")
    try:
        urlretrieve(img_url2 + ".jpg", save_path2 + iname2 + ".jpg")
    except:
        try:
            urlretrieve(img_url2 + ".gif", save_path2 + iname2 + ".gif")
        except:
            with open("./error2.txt", 'a') as f:
                f.write(img_src+"\n")


if __name__ == "__main__":
    imgs = get_imgs()
    loop(imgs)
