from datetime import datetime

from bs4 import BeautifulSoup
import requests


def countdown(config):
    target_date = datetime(*[int(x) for x in config["date"].split("/")[:3]])
    remaining_days = (target_date - datetime.now()).days
    push_data = {
        "ID": config["id"],
        "text": remaining_days,
        "icon": int(config["icon"])
    }
    awtrix_r = requests.post(config["push_url"], json=push_data)
    if awtrix_r.status_code != requests.codes.ok:
        return "failure"
    return "success"


def bilibili(config):
    r = requests.get(f"https://api.bilibili.com/x/relation/stat?vmid={config['uid']}&jsonp=jsonp")
    if r.status_code != requests.codes.ok:
        return "failure"
    resp_data = r.json()
    followers = resp_data["data"]["follower"]
    show_num = followers if followers <= 99999 else f'{round(followers / 10000, 1)}W'
    push_data = {
        "ID": config["id"],
        "text": show_num,
        "icon": int(config["icon"])
    }
    awtrix_r = requests.post(config["push_url"], json=push_data)
    if awtrix_r.status_code != requests.codes.ok:
        return "failure"
    return "success"


def weather_cn(config):
    r = requests.get(f"http://forecast.weather.com.cn/town/weather1dn/{config['town_id']}.shtml")
    if r.status_code != requests.codes.ok:
        return "failure"
    r.encoding='utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    temperature = '?' if not len(soup.select(".temp")) else soup.select(".temp")[0].text
    weather = None if not len(soup.select(".weather.dis")) else soup.select(".weather.dis")[0].text
    icon = 487
    if weather == "晴":
        icon = 349
    if weather == "阴":
        icon = 486
    if weather == "多云":
        icon = 474
    if weather == "小雨":
        icon = 346
    if weather == "雷阵雨":
        icon = 345
    if weather in ["雨", "中雨", "阵雨"]:
        icon = 477
    push_data = {
        "ID": config["id"],
        "text": temperature + "°C",
        "icon": icon
    }
    awtrix_r = requests.post(config["push_url"], json=push_data)
    if awtrix_r.status_code != requests.codes.ok:
        return "failure"
    return "success"