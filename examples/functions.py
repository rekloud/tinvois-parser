import base64
import io
import json

import PIL
import matplotlib.pyplot as plt
import requests


def perform_query(base_url, path, method='GET', headers=None, data=None):
    session = requests.Session()
    if headers is not None:
        resp = session.request(method, base_url + path, data=json.dumps(data) if data else None,
                               verify=True, headers=headers)
    else:
        resp = session.request(method, base_url + path, data=json.dumps(data))
    try:
        return resp.json()
    except Exception as e:
        print(f'json failed {e}')
        return resp


def get_image_content(image_path):
    with io.open(image_path, 'rb') as f:
        image_content = f.read()
    return base64.b64encode(image_content).decode()


def show_image(image_path, figsize=(10, 7)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(PIL.Image.open(image_path))
    return ax


def show_edges(ax, edges):
    ax.plot([e[0] for e in edges], [e[1] for e in edges], color='green')
