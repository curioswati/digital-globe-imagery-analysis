# pylint: disable= invalid-name,c-extension-no-member
'''
Download images from Digital Globe
'''

import os
import re
import sys
import time

import requests
from lxml import etree

DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please provide Home URL')
        sys.exit(1)

    home_url = sys.argv[1]

    req_session = requests.Session()
    home_resp = req_session.get(home_url)

    dom = etree.HTML(home_resp.text)

    pre_image_table_rows = dom.xpath('id("table--pre-event")//tbody/tr')
    pre_image_urls = []

    for row in pre_image_table_rows:
        pre_image_urls.extend(row.xpath(
            './td/ul//div[contains(@class, "open-data-occasion__images")]/table//tr//a/@href'
        ))
    pre_image_urls = [x for x in pre_image_urls if x.endswith('tif')]
    print('pre images: {}'.format(len(pre_image_urls)))

    post_image_table_rows = dom.xpath('id("table--post-event")//tbody/tr')
    post_image_urls = []
    for row in post_image_table_rows:
        post_image_urls.extend(row.xpath(
            './td/ul//div[contains(@class, "open-data-occasion__images")]/table//tr//a/@href'
        ))

    post_image_urls = [x for x in post_image_urls if x.endswith('tif')]
    print('post images: {}'.format(len(post_image_urls)))

    # create dir structures for both pre and post images
    event_name = home_url.split('/')[-1]
    pre_images_dir = os.path.join(DATASET_PATH, event_name, 'pre')
    if not os.path.exists(pre_images_dir):
        os.makedirs(pre_images_dir, exist_ok=True)
        print('Created: {}'.format(pre_images_dir))

    post_images_dir = os.path.join(DATASET_PATH, event_name, 'post')
    if not os.path.exists(post_images_dir):
        os.makedirs(post_images_dir, exist_ok=True)
        print('Created: {}'.format(post_images_dir))


    for url in pre_image_urls:

        # create filename
        url_split = url.split('/')
        filename = '_'.join(url_split[-3:])
        filepath = os.path.join(pre_images_dir, filename)

        if not os.path.exists(filepath) or not os.stat(filepath).st_size:
            # download image and save
            image_resp = req_session.get(url)
            with open(filepath, 'wb') as image_file:
                image_file.write(image_resp.content)
            print('Downloaded: {}'.format(filepath))
            time.sleep(2)
        else:
            print('Already Downloaded: {}'.format(filename))

    for url in post_image_urls:

        # create filename
        url_split = url.split('/')
        filename = '_'.join(url_split[-3:])
        filepath = os.path.join(post_images_dir, filename)

        if not os.path.exists(filepath) or not os.stat(filepath).st_size:
            image_resp = req_session.get(url)
            with open(filepath, 'wb') as image_file:
                image_file.write(image_resp.content)
            print('Downloaded: {}'.format(filepath))
            time.sleep(2)
        else:
            print('Already Downloaded: {}'.format(filename))
