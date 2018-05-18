
class SingerDownloader(object):

    def __init__(self, key_word, page, index, quality, store_folder):
        self.key_word = key_word
        self.page = page
        self.index = index
        self.quality = quality
        self.store_folder = store_folder

    def get_url(self):
        pass

    def get_music_hash(self, base_url):
        pass

    def get_music_download_url(self, hash_word):
        pass

    def download_music(self, download_url):
        pass
