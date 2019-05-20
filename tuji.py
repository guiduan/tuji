# -*- coding:utf-8 -*-
import requests
import re
import sys
import os
import wget


def get_urls_in_category_page(page_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    response = requests.get('http://tujixiazai.com/category/shizufangan//page/' + str(page_id) + '/', headers)
    html = response.text
    pattern = re.compile(r'<div class=\"sico\">\&gt;<\/div><a href=\"([\s\S]*?)\" title=\"')
    urls = pattern.findall(html)
    return urls


def get_download_detail_page_url(detail_page_url):
    url = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    response = requests.get(detail_page_url, headers)
    html = response.text
    pattern = re.compile(r'★免费下载地址:([\s\S]*?)\"><u>点此去下载')
    content = pattern.findall(html)
    if len(content):
        split_url = content[0].split('href="')
        if len(split_url):
            url = split_url[1]
    return url


def get_download_url(download_detail_page_url):
    download_url = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    response = requests.get(download_detail_page_url, headers)
    html = response.text
    pattern = re.compile(
        r'<big><a rel=\"external nofollow\" target=\"_blank" href=\"([\s\S]*?)\" download>下载点1')
    # pattern = re.compile(
    #   r'<big><a rel=\"external nofollow\" target=\"_blank" href=\"([\s\S]*?)\" download>下载点2')

    tmp_download_url = pattern.findall(html)
    if len(tmp_download_url):
        download_url = tmp_download_url[0]
    return download_url


def download_file(download_url, local_path=os.getcwd() + '/'):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    f = requests.get(download_url, headers)
    if f.headers.__contains__('Content-Length'):
        total_size = int(f.headers['Content-Length'])
    temp_size = 0
    file_name = download_url.split('/')[-1]
    file_name = file_name.replace('*', '')
    print('正在下载文件 ' + file_name)
    with open(local_path + file_name, 'wb') as code:
        for chunk in f.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                code.write(chunk)
                code.flush()
                if f.headers.__contains__('Content-Length'):
                    done = int(50 * temp_size / total_size)
                    sys.stdout.write("\r[%s%s ] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                    sys.stdout.flush()
    print()


def wget_file(download_url, local_path=os.getcwd() + '/'):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    file_name = download_url.split('/')[-1]
    wget.download(download_url, out=local_path + file_name)


if __name__ == '__main__':
    for page_id in range(134, 151):  # 第101页到第150页
        urls_in_category_page = get_urls_in_category_page(page_id)
        print('获取第 ' + str(page_id) + ' 页下载页面列表: ')
        print(urls_in_category_page)
        for url_in_category_page in urls_in_category_page:
            download_detail_page_url = get_download_detail_page_url(url_in_category_page)
            print('获取下载详情页: "' + download_detail_page_url + '"...')
            download_url = get_download_url(download_detail_page_url)
            print('获取下载链接: "' + download_url + '"...')
            download_file(download_url, 'W://tuji/shizufangan/')
