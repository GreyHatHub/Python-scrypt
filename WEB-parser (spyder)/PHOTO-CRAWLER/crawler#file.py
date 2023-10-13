import os
import requests

urls = [
    'http://URL/xryt/ered/files/large/1.jpg?1615792737'
]


def get_file(url):
    r = requests.get(url, stream=True)
    return r


def get_name(url):
    name = url.split('/')[-1]
    folder = name.split('.')[0]
    #if not os.path.exists(folder):
    #    os.makedirs(folder)
    #path = os.path.abspath(folder)
    #return path + '/' + name
    return name


def save_image(name, file_object):
    with open(name, 'bw') as f:
        for chunk in file_object.iter_content(8192):
            f.write(chunk)

def main():
    for i in range(143,145):
        url = f'http://URL/xryt/ered/files/large/{i}.jpg?1615792737'
        save_image(get_name(url), get_file(url))
    print("END")

if __name__ == '__main__':
    main()
