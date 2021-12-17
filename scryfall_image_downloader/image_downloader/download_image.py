import requests


def download_image(url: str, destination: str) -> None:
    try:
        with open(destination, 'wb') as image:
            image.write(requests.get(url).content)
    except Exception as e:
        print(f'Error downloading image from {url}: {e}')
