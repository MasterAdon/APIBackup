import requests
from pprint import pprint
import json
import time
from tqdm import tqdm



class VK_user:
    def __init__(self, user_id):
        self.id = user_id

    def create_yadiskfolder(self):  # Функция создания папки на Яндекс диске
        folder_name = str(input('Введите имя создаваемой папки на диске: '))
        token_Ya = str(input('Введите ключ доступа Yandex: '))
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        get_headers = {'Content-Type ': 'application/json',
                       'Authorization': 'OAuth {}'.format(token_Ya)}
        params = {'path': folder_name}
        res = requests.put(url, headers=get_headers, params=params)
        return folder_name
    folder_name = "ghjjcnj"

    def backup_vk_yandex_photo(self,):
        token_Ya = str(input('Введите ключ доступа Yandex: '))
        token_VK = str(input("Введите ключ ддоступа ВК: "))
        folder_name = str(input('Введите имя папки на диске: '))
        url_vk = 'https://api.vk.com/method/photos.get'
        params_vk = {
            'owner_id': self.id,
            'album_id': 'profile',
            'access_token': token_VK,
            'v': '5.130',
            'extended': '1',
        }

        url_ya = "https://cloud-api.yandex.net:443/v1/disk/resources/upload"
        get_headers = {'Content-Type ': 'application/json',
                       'Authorization': 'OAuth {}'.format(token_Ya)}
        res = requests.get(url_vk, params=params_vk)
        a = res.json()  # Ответ на запрос по фотографиям
        c = []  # Список с фотографиями, который наполним ниже
        for key, va in a.items():
            for f in va['items']:
                fot = f['sizes'][-1]['url']
                typ = f['sizes'][-1]['type']
                fi_name = f['likes']['count']
                file_na = f['id']
                dict_fot = {'size': typ, 'file_name': f'{fi_name}.jpg'}
                params_ya = {
                    'url': fot,
                    'path': f"{folder_name}/{dict_fot['file_name']}", 'overwrite': 'true'}
                respose = requests.post(url_ya, headers=get_headers, params=params_ya) # Сделали копирование
                c.append(dict_fot)
        with open(f'{self.id}.json', 'w', encoding='utf-8') as write_file:  # Создали .json файл
            json.dump(c, write_file)
        for i in tqdm(c):
                  time.sleep(0.5)
        return



user = VK_user(input('Введите Id номер аккаунта: '))
result = user.backup_vk_yandex_photo()




