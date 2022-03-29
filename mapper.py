import contextlib
import os
import queue
import requests
import sys
import threading
import time

FILTERED = [".jpg", ".png", ".gif", ".css"]
TARGET = "http://vaithiyaainterior.com/wordpress"
THREAD = 10

answers = queue.Queue()
web_paths = queue.Queue()


def gather_path():
    for root, _, files in os.walk('.'):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)


@contextlib.contextmanager
def chidir(path):
    """
    on enter, change directory to specified  path
    on exit, change directory back to original
    """
    this_dir = os.getcwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(this_dir)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        time.sleep(2)
        r = requests.get(url)
        if r.status_code == '200':
            answers.put(url)
            sys.stdout.write('+')
        else:
            sys.stdout.write('X')
        sys.stdout.flush()


def run():
    mythreads = list()
    for i in range(THREAD):
        print(f'Spawning thread {i}.')
        t = threading.Thread(target=test_remote())
        mythreads.append(t)

    for thread in mythreads:
        thread.join()


if __name__ == '__main__':
    with chidir('/home/kali/Downloads/wordpress'):
        gather_path()
    print(' Press return to continue.')

    run()
    with open('mytexts.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print('done')
