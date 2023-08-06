import os
import math

import requests
from urllib.parse import urljoin
from urllib.parse import urlsplit

def download_media(api, media, out_path):
    """ Download a media file from Tator to an off-line location.

    Example:

    .. code-block:: python

        api = tator.get_api(host, token)
        media = api.get_media(media_id)
        out_path = f'/tmp/{media.name}'
        for progress in tator.util.download_media(api, media, out_path):
            print(f"Download progress: {progress}%")

    :param api: :class:`tator.TatorApi` object.
    :param media: :class:`tator.Media` object.
    :param path-like out_path: Path to where to download.
    :returns: Generator the yields progress (0-100).
    """
    config = api.api_client.configuration
    host = config.host
    token = config.api_key['Authorization']
    prefix = config.api_key_prefix['Authorization']
    if media.media_files is not None:
        archival = media.media_files.archival
        streaming = media.media_files.streaming
        if len(archival) > 0:
            url = urljoin(host, archival[0].path)
        elif len(streaming) > 0:
            url = urljoin(host, streaming[0].path)
    else:
        # Legacy way of using streaming prior to streaming
        # and images
        url = f"media/{media.file}"
        if media.original:
            url = f"data/raw/{media.original}"
        url = urljoin(host, url)

    # Supply token here for eventual media authorization
    headers = {
        'Authorization': f'{prefix} {token}',
        'Content-Type': f'application/json',
        'Accept-Encoding': 'gzip',
    }
    CHUNK_SIZE = 2 * 1024 * 1024
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        total_size = r.headers['Content-Length']
        total_chunks = math.ceil(int(total_size) / CHUNK_SIZE)
        chunk_count = 0
        last_progress = 0
        yield last_progress
        with open(out_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    chunk_count += 1
                    f.write(chunk)
                    this_progress = round((chunk_count / total_chunks) *100,1)
                    if this_progress != last_progress:
                        yield this_progress
                        last_progress = this_progress
        yield 100
