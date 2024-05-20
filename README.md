## Flickr Album Downloader

### Features
- enables users to download entire albums from Flickr
- download photos in the highest available quality
- automate the process of album downloading

### Installation
1. Clone the repository

```bash
git clone https://github.com/ccyhui/flickr-album-dl
cd flickr-album-dl
pip install -r requirements.txt
```

2. Ensure you have a compatible web driver for Selenium installed. (I recommend using Firefox as it's the web driver I used in my code.)

## How to download the album using Flickr-album-dl?
1. Navigate to the Flickr's album page which you want to download. The URL should look something like this:
`https://www.flickr.com/photos/<path_alias>/albums/<photoset_id>`

2. Open the `album_info.yaml` file in a text editor and input the <path_alias> and <photoset_id> in the respective fields. The file should look like this:

```yaml
path_alias: <path_alias>
photoset_id: <photoset_id>
base_url: https://www.flickr.com/photos
```

3. Run the Python script using `python download_album.py`.
