from selenium.webdriver.firefox.options import Options as FirefoxOptions
from seleniumwire import webdriver
import requests
import time
import re
import os
import yaml

def is_scraped(album_info):
    dir_path = os.path.join('./downloads', f'{album_info['path_alias']}', f'{album_info['photoset_id']}')
    if os.path.exists(dir_path):
        return True
    else:
        return False

def get_xhr_request(target_url, timeout=10):
    pattern = r'^https://api.flickr.com/services/rest\?.*method=flickr.autosuggest.getContextResults'
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(target_url)
    request = driver.wait_for_request(pattern, timeout)
    driver.quit()
    return request

def get_photosets_api_url(request, photoset_id):
    pattern = r'&?method=([^&]*)'
    if re.search(pattern, request.url):
        photosets_api_url = re.sub(pattern, '&method=flickr.photosets.getPhotos', request.url)
        return photosets_api_url + f'&photoset_id={photoset_id}&page=1&per_page=100'

def get_highest_quality_photos_url(api_url, urls=[]):
    response = requests.get(api_url)
    album = response.json()['photoset']

    for photo in album['photo']:
        candidates = {key: value for key, value in photo.items() if (key.startswith('height') or key.startswith('width')) and isinstance(value, (int, float))}
        url_key = re.sub(r'^([^_]+)', 'url', max(candidates, key=candidates.get))
        urls.append(photo[url_key])
    
    current_page = int(album['page'])
    total_pages = int(album['pages'])
    if current_page < total_pages:
        api_url = re.sub(r'&page=([^&]*)', f'&page={current_page+1}', api_url)
        time.sleep(1)
        return get_highest_quality_photos_url(api_url, urls=urls)
    else:
        return urls

def download_album(album_info_path='./album_info.yaml', album_directory='./downloads'):
    with open(album_info_path, 'r') as f:
        album_info = yaml.safe_load(f)
    if is_scraped(album_info):
        print('Already downloaded!')
        return
    target_url = f'{album_info['base_url']}/{album_info['path_alias']}/albums/{album_info['photoset_id']}'
    request = get_xhr_request(target_url)
    api_url = get_photosets_api_url(request, album_info['photoset_id'])
    urls = get_highest_quality_photos_url(api_url)
    
    directory = f'{album_directory}/{album_info['path_alias']}/{album_info['photoset_id']}'
    os.makedirs(directory, exist_ok=True)
    num_dl = 0
    for url in urls:
        filename = url.split('/')[-1]
        filepath = os.path.join(directory, filename)
        response = requests.get(url)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        num_dl += 1
        if num_dl % 10 == 0 and num_dl != 0:
            print(f'Downloaded {num_dl} images!')
    print(f'Done! Downloaded a total of {num_dl} images!')

if __name__ == '__main__':
    download_album()
