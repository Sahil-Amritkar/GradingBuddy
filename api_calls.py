import requests
import json
API_KEY = open("api_key.txt", "r").read()

def get_synonyms(word=None):
    api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    if response.status_code == requests.codes.ok:
        response = json.loads(response.text)
        return response['synonyms']
    else:
        print("Error:", response.status_code, response.text)

def get_cosine_similarity(text1, text2):
    body = { 'text_1': text1, 'text_2': text2 }
    api_url = 'https://api.api-ninjas.com/v1/textsimilarity'
    response = requests.post(api_url, headers={'X-Api-Key': API_KEY}, json=body)
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

def get_image_to_text(image_path):
    api_url = 'https://api.api-ninjas.com/v1/imagetotext'
    image_file_descriptor = open(image_path, 'rb')
    files = {'image': image_file_descriptor}
    response = requests.post(api_url, headers={'X-Api-Key': API_KEY}, files=files)
    if response.status_code == requests.codes.ok:
        response = json.loads(response.text)
        scanned_text=''
        for obj in response:
            scanned_text=scanned_text+' '+obj["text"]
        return scanned_text.strip()
    else:
        print("Error:", response.status_code, response.text)
