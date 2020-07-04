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
        "icon": "vultr"
    }
    awtrix_r = requests.post(config["push_url"], json=push_data)
    if awtrix_r.status_code != requests.codes.ok:
        return "failure"
    return "success"
    