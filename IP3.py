import requests
import os
url = "https://api.ipdata.co?api-key\
=d99106e16b9472a9372a3769674d33850d600279587bbad650db3e52"
api_key2 = os.environ.get('api_key')
# Set the API key as a header
headers = {'api-key': api_key2}
specific_url = "https://api.ipdata.co/189.154.184.127?api-key\
=d99106e16b9472a9372a3769674d33850d600279587bbad650db3e52"


def getLocation():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('error')
