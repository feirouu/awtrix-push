import requests

def vultr(config):
    r = requests.get("https://api.vultr.com/v1/server/list", headers={
        "API-Key": config["token"]
    })
    if r.status_code != requests.codes.ok:
        return
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
    
    requests.post(config["push_url"], json=push_data)


def bilibili(config):
    r = requests.get(f"https://api.bilibili.com/x/relation/stat?vmid={config['uid']}&jsonp=jsonp")
    if r.status_code != requests.codes.ok:
        return
    resp_data = r.json()
    push_data = {
        "ID": config["id"],
        "text": resp_data["data"]["follower"],
        "icon": config["icon"]
    }

    requests.post(config["push_url"], json=push_data)
