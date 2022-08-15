import requests
from unittest import TestCase
import json


YA_TOKEN = 'secret_token'
YA_DIR = 'New_dir'
url = 'https://cloud-api.yandex.net/v1/disk/resources'
params = {'path': YA_DIR}
headers = {'Authorization': f'OAuth {YA_TOKEN}'}


class TestYaDirUnitTest(TestCase):
    def test_unauthorized(self):
        headers = {'Authorization': f'OAuth '}  # Проверка на введение правильного токена
        res = requests.put(url, params=params, headers=headers)
        self.assertEqual(res.status_code, 401)  # Пользователь не авторизован

    def test_create(self):
        res = requests.put(url, params=params, headers=headers)   # Добавляем новую папку
        self.assertEqual(res.status_code, 201)  # Проверяем статус код
        res = requests.get(url, params=params, headers=headers)
        item_type = json.loads(res.text)['type']
        item_name = json.loads(res.text)['name']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(item_type, 'dir')
        self.assertEqual(item_name, YA_DIR)
        res = requests.delete(url, params=params, headers=headers)  # Удаляем папку
        self.assertEqual(res.status_code, 204)  # Проверяем статус код

    def test_create_already_exist(self):
        res = requests.put(url, params=params, headers=headers)  # Добавляем новую папку
        self.assertEqual(res.status_code, 201)  # Проверяем, если добавление прошло успешно
        res = requests.put(url, params=params, headers=headers)  # Конфликт при попытке создания одинаковой папки
        self.assertEqual(res.status_code, 409)
        res = requests.delete(url, params=params, headers=headers)  # Удаляем папку
        self.assertEqual(res.status_code, 204)  # Проверяем статус код
