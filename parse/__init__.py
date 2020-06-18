import requests

def vultr(config):
    r = requests.get(config["api_url"], headers={
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
