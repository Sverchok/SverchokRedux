import bpy

import json
from urllib.request import urlopen
import webbrowser
import time

"""
zeffii 13 Dec 2015:
It might be possible to remove the check for hasattr(this, 'readall'),
and use this.read().decode() everywhere. it looks fugly.

"""


def decode_url(parsable):
    if hasattr(parsable, 'readall'):
        return parsable.readall().decode()
    else:
        return parsable.read().decode()


def process_upload(gist_files_dict, project_name, public_switch):

    if len(gist_files_dict) == 0:
        print("nothing to send!")
        return

    pf = time.strftime("_%Y_%m_%d_%H-%M")
    gist_post_data = {
        'description': project_name + pf,
        'public': public_switch,
        'files': gist_files_dict}

    json_post_data = json.dumps(gist_post_data).encode('utf-8')

    def get_gist_url(found_json):
        wfile = json.JSONDecoder()
        wjson = wfile.decode(found_json)
        gist_url = 'https://gist.github.com/' + wjson['id']

        print(gist_url)
        webbrowser.open(gist_url)
        # or just copy url to clipboard?

    def upload_gist():
        print('sending')
        url = 'https://api.github.com/gists'

        json_to_parse = urlopen(url, data=json_post_data)
        print('received response from server')

        found_json = decode_url(json_to_parse)
        get_gist_url(found_json)

    upload_gist()


def upload(file_names, project_name='noname', public_switch=True):
    """
    Usage:
    - file_names is a list of file_names currently loaded in bpy.data.texts
    - project_name is the name you wish to give to the gist
    - public_switch allows you to keep the anonymous gist secret (hidden from search)
    """
    gist_files_dict = {}
    for f in file_names:
        tfile = bpy.data.texts.get(f)
        if tfile:
            file_content = tfile.as_string()
            gist_files_dict[f] = {"content": file_content}

    process_upload(gist_files_dict, project_name, public_switch)


# Gists can contain multiple files, we'll download all by default.

def download(gist_id):
    """
    Usage: download('922e5378c1ff87399f62')
    - this will download all files and content of the gist as new textblocks
    - if a file already exists locally, the new download will get the timestamp appended

    """

    def get_raw_urls_from_gist_id(gist_id):

        gist_id = str(gist_id)
        url = 'https://api.github.com/gists/' + gist_id

        found_json = decode_url(urlopen(url))
        wfile = json.JSONDecoder()
        wjson = wfile.decode(found_json)

        # 'files' may contain several - this will mess up gist name.
        files_flag = 'files'
        file_names = list(wjson[files_flag].keys())
        names_to_urls_dict = {f: wjson[files_flag][f]['raw_url'] for f in file_names}
        return names_to_urls_dict

    texts = bpy.data.texts
    files_dict = get_raw_urls_from_gist_id(gist_id)
    pf = time.strftime("_%Y_%m_%d_%H-%M")

    for file_name, url in files_dict.items():
        if file_name in texts:
            t = texts.new(file_name + pf)
        else:
            t = texts.new(file_name)

        content = decode_url(urlopen(url))
        t.from_string(content)
