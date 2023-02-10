from bs4 import BeautifulSoup as bs
from Cryptodome.Cipher import AES
import base64
import json
import yarl
import requests

s = b'37911490979715163134003223491201'
s_2 = b'54674138327930866480207815084989'
iv = b'3134003223491201'


def get_crypto(url):
    '''
    function to get crypto data
    '''
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    for item in soup.find_all('script', attrs={'data-name': 'episode', 'data-value': True}):
        crypto = str(item['data-value'])
    return crypto


def pad(data):
    '''
    helper function
    '''
    return data + chr(len(data) % 16) * (16 - len(data) % 16)


def decrypt(key, data):
    '''
    function to decrypt data
    '''
    return AES.new(key, AES.MODE_CBC, iv=iv).decrypt(base64.b64decode(data))


def extract_m3u8(link):
    crypto_data = get_crypto(link)
    decrypted_crypto = decrypt(s, crypto_data)
    new_id = decrypted_crypto[decrypted_crypto.index(b"&"):].strip(
        b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10").decode()
    p_url = yarl.URL(link)
    ajax_url = "https://{}/encrypt-ajax.php".format(p_url.host)

    encrypted_ajax = base64.b64encode(
        AES.new(s, AES.MODE_CBC, iv=iv).encrypt(
            pad(p_url.query.get('id')).encode()
        )
    )

    r = requests.get(
        f'{ajax_url}?id={encrypted_ajax.decode()}{new_id}&alias={p_url.query.get("id")}',

        headers={'x-requested-with': 'XMLHttpRequest'}
    )

    j = json.loads(
        decrypt(s_2, r.json().get("data")).strip(
            b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10"
        )
    )

    return j['source'][0]['file']
