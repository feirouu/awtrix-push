from bs4 import BeautifulSoup
import requests

def vultr(config):
    r = requests.get("https://api.vultr.com/v1/server/list", headers={
        "API-Key": config["token"]
    })
    if r.status_code != requests.codes.ok:
        return "failure"
    resp_data = r.json()
    remaining = round(float(resp_data[config["subid"]]["allowed_bandwidth_gb"]) - float(resp_data[config["subid"]]["current_bandwidth_gb"]), 1)
    push_data = {
        "ID": config["id"],
        "text": f'{remaining}G',
        "icon": [0, 0, 0, 0, 0, 0, 0, 0,
            0, 65535, 65535, 0, 669, 669, 0, 0,
            0, 5468, 5468, 0, 669, 669, 669, 0,
            0, 669, 669, 0, 0, 669, 669, 0,
            0, 669, 669, 669, 0, 0, 0, 0,
            0, 0, 669, 669, 669, 0, 0, 0,
            0, 0, 0, 669, 669, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
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
    push_data = {
        "ID": config["id"],
        "text": resp_data["data"]["follower"],
        "icon": config["icon"]
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
