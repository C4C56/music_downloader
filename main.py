# coding=utf-8
import argparse
from music_downloader import MusicDownloader
from singer_downloader import SingerDownloader


def main():
    parser = argparse.ArgumentParser(prog='KuGou music crawler')
    group_development = parser.add_argument_group('group development', 'group development used for development')
    group_development.add_argument('--search_type', default='music', choices=['music', 'singer'], help='choose the type of your result that you are seraching for')
    group_development.add_argument('--key_word', help='the word you search')
    group_development.add_argument('--page', default='ALL', help='the page of the music that you are searching')
    group_development.add_argument('--index', default='ALL', help='the index of the music in its page')
    group_development.add_argument('--quality', default='normal', choices=['normal', 'high', 'best'], help='the quality that you want to download')
    group_development.add_argument('--store_folder', default='/home/mao/Desktop/music/', help='the music download path')
    args = parser.parse_args()
    search_type = args.search_type
    key_word = args.key_word
    page = args.page
    index = args.index
    quality = args.quality
    store_folder = args.store_folder
    if search_type == 'music':
        downloader = MusicDownloader(key_word, page, index, quality, store_folder)
    else:
        downloader = SingerDownloader(key_word, page, index, quality, store_folder)
    base_url_list = downloader.get_url()
    hash_dict = downloader.get_music_hash(base_url_list)
    download_url_dict = downloader.get_music_download_url(hash_dict)
    downloader.download_music(download_url_dict)


if __name__ == '__main__':
    main()
