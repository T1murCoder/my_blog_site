'''
Данный скрипт предназначен для работы с API этого сайта

Выбор ресурса: posts/users (обязательный параметр)
id: id в базе данных (необязательный параметр)
token: ключ для доступа к API (обязательный параметр)
method: метод запроса (необязательный параметр, по дефолту = 'get')
json: файл с данными для отправления вместе с запросом (необязательный параметр)
'''

import argparse
import requests
import sys
import json


parser = argparse.ArgumentParser(
    description="Данный скрипт облегчает работу с api, этого сайта"
)
parser.add_argument("resource", metavar="resource", choices=['posts', 'users'], help="one of: [posts/users]")
parser.add_argument("id", nargs="?", metavar="id", default=None, help="id of user/post")
parser.add_argument("--token", required=True, help="your personal access token")
parser.add_argument("--method", choices=['get', 'delete', 'post'], default='get', help="request method")
parser.add_argument("--json", default=None, help="your json")


def make_request(url, method, json_arg=None):
    if method == 'get':
        response = requests.get(url)
    elif method == 'delete':
        response = requests.delete(url)
    elif method == 'post':
        if json_arg:
            with open(json_arg) as f:
                data = json.load(f)
            response = requests.post(url, json=data)
        else:
            response = requests.post(url)
    return response


if __name__ == "__main__":
    args = parser.parse_args()
    
    dt = {
        'posts': 'news_posts',
        'users': 'users'
    }
    
    url = "http://localhost:8080/api/v2/"
    resource = args.resource
    arg_id = args.id
    token = args.token
    method = args.method
    json_arg = args.json
    if arg_id:
        if not (method in ['get', 'delete']):
            print("Incorrect method")
            sys.exit(1)
    
    url = url + dt[resource] + '/'
    if arg_id:
        url = url + arg_id + '/'
    url = url + "token=" + token
    
    print(url)
    response = make_request(url, method, json_arg)
    print(response)
    print(response.json())