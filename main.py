import requests


def getPred(inp):
    url = "https://discriminate.grover.allenai.org/api/disc"

    payload = {
        "article": f"{inp}",
        "domain": "",
        "date": "",
        "authors": "",
        "title": "",
        "target": "discrimination"
    }
    headers = {
        "authority": "discriminate.grover.allenai.org",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json;charset=UTF-8",
        "dnt": "1",
        "origin": "https://grover.allenai.org",
        "referer": "https://grover.allenai.org/",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()['groverprob']


print(getPred(input()))
