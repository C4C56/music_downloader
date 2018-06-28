import json
import math
import urllib
from urllib.request import urlretrieve
import requests


class MusicDownloader(object):

    def __init__(self, key_word, page, index, quality, store_folder):
        self.key_word = urllib.parse.quote(key_word)
        self.page = page
        self.index = index
        self.quality = quality
        self.store_folder = store_folder + '/'

    @staticmethod
    def get_download_url_by_quality(quality, hash_dict):
        base_hash_url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash={}'
        if quality == 'best':
            try:
                detail_url = base_hash_url.format(hash_dict[quality])
            except:
                print(hash_dict['file_name'] + " don't have best quality music")
                print("we are trying to download high quality music for you")
                quality = 'high'
                return MusicDownloader.get_download_url_by_quality(quality, hash_dict)
            response = requests.get(detail_url)
            data_json = json.loads(response.text)
            if data_json['data']['play_url']:
                return data_json['data']['play_url']
            else:
                print(hash_dict['file_name'] + " don't have best quality music")
                print("we are trying to download high quality music for you")
                quality = 'high'
                return MusicDownloader.get_download_url_by_quality(quality, hash_dict)
        if quality == 'high':
            try:
                detail_url = base_hash_url.format(hash_dict[quality])
            except:
                print(hash_dict['file_name'] + " don't have high quality music")
                print("we are trying to download normal quality music for you")
                quality = 'normal'
                return MusicDownloader.get_download_url_by_quality(quality, hash_dict)
            response = requests.get(detail_url)
            data_json = json.loads(response.text)
            if data_json['data']['play_url']:
                return data_json['data']['play_url']
            else:
                print(hash_dict['file_name'] + " don't have high quality music")
                print("we are trying to download normal quality music for you")
                quality = 'normal'
                return MusicDownloader.get_download_url_by_quality(quality, hash_dict)
        if quality == 'normal':
            try:
                detail_url = base_hash_url.format(hash_dict[quality])
            except:
                print(hash_dict['file_name'] + " don't have normal quality music")
                print("Sorry, we can't download this music for you")
                return None
            response = requests.get(detail_url)
            data_json = json.loads(response.text)
            if data_json['data']['play_url']:
                return data_json['data']['play_url']
            else:
                print(hash_dict['file_name'] + " don't have normal quality music")
                print("Sorry, we can't download this music for you")
                return None

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
        print("finish get music message")
        return base_url_list

    def get_music_hash(self, base_url_list):
        hash_dict_list = []
        if self.index == 'ALL':
            for base_url in base_url_list:
                response = requests.get(base_url)
                json_data = json.loads(response.text)
                for music_info in json_data['data']['info']:
                    hash_dict = dict()
                    hash_dict['file_name'] = music_info['filename']
                    if music_info['hash']:
                        hash_dict['normal'] = music_info['hash']
                    if music_info['320hash']:
                        hash_dict['high'] = music_info['320hash']
                    if music_info['sqhash']:
                        hash_dict['best'] = music_info['sqhash']
                    hash_dict_list.append(hash_dict)
        else:
            index_number = int(self.index) - 1
            for base_url in base_url_list:
                hash_dict = dict()
                response = requests.get(base_url)
                json_data = json.loads(response.text)
                music_info = json_data['data']['info'][index_number]
                hash_dict['file_name'] = music_info['filename']
                if music_info['hash']:
                    hash_dict['normal'] = music_info['hash']
                if music_info['320hash']:
                    hash_dict['high'] = music_info['320hash']
                if music_info['sqhash']:
                    hash_dict['best'] = music_info['sqhash']
                hash_dict_list.append(hash_dict)
        print("finish get music hash")
        return hash_dict_list

    def get_music_download_url(self, hash_dict_list):
        download_url_dict = {}
        for hash_dict in hash_dict_list:
            download_url = MusicDownloader.get_download_url_by_quality(self.quality, hash_dict)
            if download_url:
                download_url_dict[hash_dict['file_name']] = download_url
        print("finish get music download url")
        return download_url_dict

    def download_music(self, download_url_dict):
        print("start download music")
        for filename in download_url_dict.keys():
            last_name = download_url_dict[filename].split('.')[-1]
            store_path = self.store_folder + filename + '.' + last_name
            try:
                urlretrieve(download_url_dict[filename], filename=store_path)
                print ('download ' + filename + ' success')
            except Exception as e:
                print ('download ' + filename + 'failed because of ' + e)
        print("finish download music")
