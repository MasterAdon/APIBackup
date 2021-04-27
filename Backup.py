import requests
from pprint import pprint
import json
import time
from tqdm import tqdm



class VK_user:
    def __init__(self, user_id):
        self.id = user_id



class Ya_disk:
    def __init__(self, token):
        self.token = token

    def create_yadiskfolder(self):
        """ Метод для создания папки на Яндекс диске """
        folder_name = str(input('Введите имя создаваемой папки на диске: '))
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        get_headers = {'Content-Type ': 'application/json',
                       'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': folder_name}
        requests.put(url, headers=get_headers, params=params)
        return folder_name

    def upload_yadisk_post(self, folder_name, upload_list_photo):
        """ Метод для загрузки файлов на Яндекс диск напрямую из сети """
        url_ya = "https://cloud-api.yandex.net:443/v1/disk/resources/upload"
        get_headers = {'Content-Type ': 'application/json',
                       'Authorization': 'OAuth {}'.format(self.token)}
        for i in upload_list_photo:
            params_ya = {'url': i['file_path'],
                         'path': f"{folder_name}/{i['file_name']}", 'overwrite': 'true'}
            response = requests.post(url_ya, headers=get_headers, params=params_ya) # Сделали копирование на Яндекс диск
        for t in tqdm(upload_list_photo):
            time.sleep(0.5)
        if response.status_code == 202:
            return print('Копирование выполнено')



class VK_api(VK_user):
    def __init__(self, user_id, token):
        super().__init__(user_id)
        self.token = token

    def backup_vk_photo(self):
        """Метод для извлечения и сортировки фотографий ВК профиля"""
        url_vk = 'https://api.vk.com/method/photos.get'
        params_vk = {'owner_id': self.id,
                     'album_id': 'profile',
                     'access_token': self.token,
                     'v': '5.130',
                     'extended': '1'}
        response = requests.get(url_vk, params=params_vk)
        foto_response_dict = response.json()  # Ответ на запрос по фотографиям в виде словаря .json
        upload_list_foto =[]  #Список с фотографиями для дальнейшей работы
        for key, value in foto_response_dict.items():
            for f in value['items']:
                foto_path = f['sizes'][-1]['url']
                type_photo = f['sizes'][-1]['type']
                foto_likes = f['likes']['count']
                foto_data = f['date']
                dict_foto = {'size': type_photo, 'file_name': f'{foto_data}Like{foto_likes}.jpg', 'file_path': f'{foto_path}'}
                upload_list_foto.append(dict_foto)
        return upload_list_foto


    def create_jsonfile(self, upload_list_foto):
        """ Метод создания .json файла """
        foto_list = []
        for i in upload_list_foto:
            del i['file_path']
            foto_list.append(i)
        with open(f'{self.id}.json', 'w', encoding='utf-8') as write_file:  # Создали .json файл
            json.dump(foto_list, write_file)
        return




# Тестируем методы классов, на основании параметров задания

# Ключи доступа к сервесам храняться в файле tokens.txt по порядку:
# 1-я строка Яндекс ключ
# 2-я строка ВК ключ

with open('tokens.txt', encoding='utf-8') as f:
    token_Ya = f.readline().strip()
    token_VK = f.readline().strip()




user = str(input("Введите ID номер пользователя: "))
user_vk = VK_api(user, token_VK)
user_ya = Ya_disk(token_Ya)
upload_list = user_vk.backup_vk_photo()
folder_copy = user_ya.create_yadiskfolder()
user_ya.upload_yadisk_post(folder_copy, upload_list)
file_json = user_vk.create_jsonfile(upload_list)



