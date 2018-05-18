import json
import math
import urllib
from urllib import urlretrieve
import requests


class MusicDownloader(object):

    def __init__(self, key_word, page, index, quality, store_folder):
        self.key_word = urllib.quote(key_word)
        self.page = page
        self.index = index
        self.quality = quality
        self.store_folder = store_folder

    def get_url(self):
        base_url_pattern = 'http://mobilecdn.kugou.com/api/v3/search/song?&plat=0&version=8969&keyword={}&page={}&pagesize=30'
        base_url_list = []
        if self.page == 'ALL':
            url = base_url_pattern.format(self.key_word, 1)
            response = requests.get(url)
            json_data = json.loads(response.text)
            count = float(json_data['data']['total'])
            page_count = int(math.ceil(count/30))
            for i in range(1, page_count+1):
                url = base_url_pattern.format(self.key_word, i)
                base_url_list.append(url)
        else:
            url = base_url_pattern.format(self.key_word, self.page)
            base_url_list.append(url)
        return base_url_list

    def get_music_hash(self, base_url_list):
        hash_dict = {}
        if self.index == 'ALL':
            for base_url in base_url_list:
                response = requests.get(base_url)
                json_data = json.loads(response.text)
                for music_info in json_data['data']['info']:
                    if self.quality == 'normal':
                        if music_info['hash']:
                            hash_dict[music_info['filename']] = music_info['hash']
                        else:
                            print ('{} dont have normal quality music'.format(music_info['filename']))
                    elif self.quality == 'high':
                        if music_info['320hash']:
                            hash_dict[music_info['filename']] = music_info['320hash']
                        else:
                            print ('{} dont have high quality music'.format(music_info['filename']))
                    else:
                        if music_info['sqhash']:
                            hash_dict[music_info['filename']] = music_info['sqhash']
                        else:
                            print ('{} dont have best quality music'.format(music_info['filename']))
        else:
            index_number = int(self.index) - 1
            for base_url in base_url_list:
                response = requests.get(base_url)
                json_data = json.loads(response.text)
                music_info = json_data['data']['info'][index_number]
                if self.quality == 'normal':
                    if music_info['hash']:
                        hash_dict[music_info['filename']] = music_info['hash']
                    else:
                        print ('{} dont have normal quality music'.format(music_info['filename']))
                elif self.quality == 'high':
                    if music_info['320hash']:
                        hash_dict[music_info['filename']] = music_info['320hash']
                    else:
                        print ('{} dont have high quality music'.format(music_info['filename']))
                else:
                    if music_info['sqhash']:
                        hash_dict[music_info['filename']] = music_info['sqhash']
                    else:
                        print ('{} dont have best quality music'.format(music_info['filename']))
        return hash_dict

    def get_music_download_url(self, hash_dict):
        download_url_dict = {}
        base_hash_url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash={}'
        for filename in hash_dict.keys():
            detail_url = base_hash_url.format(hash_dict[filename])
            response = requests.get(detail_url)
            data_json = json.loads(response.text)
            if data_json['data']['play_url']:
                download_url_dict[filename] = data_json['data']['play_url']
            else:
                print('{} dont have {} quality music'.format(filename, self.quality))
        return download_url_dict

    def download_music(self, download_url_dict):
        for filename in download_url_dict.keys():
            last_name = download_url_dict[filename].split('.')[-1]
            store_path = self.store_folder + filename + '.' + last_name
            try:
                urlretrieve(download_url_dict[filename], filename=store_path)
                print ('download' + filename + 'sucess')
            except Exception as e:
                print ('download ' + filename + 'failed because of ' + e.message)

