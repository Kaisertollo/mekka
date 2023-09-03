import random
import string
import json
import requests
import bcrypt
def generate_code():
    characters = string.digits
    code = ''.join(random.choice(characters) for _ in range(5))
    return code
def hashPassword(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'))
    return hashed_password

   
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
def create_marchand(name,type,email,role_id,phone,cos):
    url = "http://payment.mekka-africa.com/api/v1/creation-compte-marchand"
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYTg3MTI3NzNkYzRjNzE4YjNkNGZiMWViMDA5OWJkN2ViNTA0NjQ1MzkxNDAxYjNkMjM0MzA1MzljMWI3MmNmOWYzMDJkNGMyNDZhZTU5MmIiLCJpYXQiOjE2OTE2MjAyMDkuOTcxOTk3LCJuYmYiOjE2OTE2MjAyMDkuOTcyMDAyLCJleHAiOjE3MjMyNDI2MDkuOTYzNDg3LCJzdWIiOiI0Iiwic2NvcGVzIjpbXX0.RBpaGn6l6eZxrVc0tiFak-fsZKQjxE5NGtIfM4QydB9R7YNKuH0-ypEAAxYh82A5sav9yWmhX5Fa4ha_ieQ0SbuidOARQVDtc3D7AXptJX_go36Virz5ehaz39aWTf5i9dQqdgypprLya8DGPGhX92fuJQFrDdF_1S2-9U0VuxbLoSLIgBgJxsEDUaEdIwx5SzsOGMcClaG_cjhp-lpSKolQZ6VbYKWt77H4orOznF8ebzkzrK7QfU4f9MiruQNlJvBvlkIXESLqRfgRI3739jmqAMgmWrGWNIWarcrMsW6ymhD9cnaz-PeMVG084zXr3Umn5xobgIe0gTFd3bsQU09sq_QgHqW27pvwsd21jTMfLNyltC4l3NbE2BiRWNDwJhLDVeRXACSasLe00xQ1BWDlAQQUi92v565XdZIt60VOZmUc4Qe9Q-qz6Dcmo6seSbWm84DH9n-e3D0EiAt7RTNhUSFMOrJ4EJJWwtorWLiTvKw7tbogKtJuL0_TBf_lIfiY-Td-N9byodQX-lhI5M05m-_cnUw7vOxvVSrRI5ZElrWBb3jiAEGC5Bhl8fr0KBt0L5z2-Mre4U1QJrg6MKcDT4enOHqgSDRTZBOhAXxvvtUDSKGtmFt9u84LmU-b__AKvP2NImklk_J164nP-VuVMv5OCmGEJmChZF46l6Q"
    data= {
	"prenom": name,
	"nom": type,
	"second_nom": "",
	"sexe": "M",
	"dob": "1994-05-02",
	"pob": "Kinshasa",
	"mobile": phone,
	"phone": phone,
	"email": email,
	"numero_rue": "53",
	"rue": "Mokoyo",
	"quartier": "Mbinza",
	"pays_id": 1,
	"ville": "Kinshasa",
	"roles_id": role_id,
	"cos": cos,
	"password": "123456"}
    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json' 
    }
    response = requests.post(url,json=data,headers=headers)
    print(f"vlad {response.status_code}")
    if response.status_code == 200 or response.status_code == 201:
        return True
    else:
        return False

