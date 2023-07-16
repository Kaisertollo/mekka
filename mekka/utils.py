import requests
import json
def Send_wp(phone,code):
    url = "https://api.ultramsg.com/instance46277/messages/chat"

    payload = json.dumps({
        "token": "ucl1zdrrlnekz30x",
        "to": phone,
        "body": f"Votre code de connexion est :{code}"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)