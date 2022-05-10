import sys
import socket
import random
import time
import requests
import os

TCP_IP = "0.0.0.0"
TCP_PORT = 9999
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
token = os.getenv('TOKEN')
urls = [
    'https://api.github.com/search/repositories?q=+language:Python&sort=updated&order=desc&per_page=50',
    'https://api.github.com/search/repositories?q=+language:Java&sort=updated&order=desc&per_page=50',
    'https://api.github.com/search/repositories?q=+language:CSharp&sort=updated&order=desc&per_page=50'
]

DELIMITER = '$#(DELIMITER)#$'

s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
# if the connection is accepted, proceed
conn, addr = s.accept()
print("Connected... Starting sending data.")
while True:
    try:
        for url in urls:
            res = requests.get(url, headers={"Authorization": "token " + token})
            result_json = res.json()
            for item in result_json["items"]:
                data = ""
                if item["description"] is not None:
                    data = f'{item["name"]}{DELIMITER}{item["language"]}{DELIMITER}{item["stargazers_count"]}{DELIMITER}{item["description"]}\n'
                else:
                    data = f'{item["name"]}{DELIMITER}{item["language"]}{DELIMITER}{item["stargazers_count"]}{DELIMITER} \n'
                conn.send(data.encode())
                print(data)
        time.sleep(15)
    except KeyboardInterrupt:
        s.shutdown(socket.SHUT_RD)