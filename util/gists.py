import bpy

import json
from urllib.request import urlopen
import webbrowser
import time


# def find_filenames():
#     filenames = set()
#     for window in bpy.context.window_manager.windows:
#         for area in window.screen.areas:

#             if not area.type == 'TEXT_EDITOR':
#                 continue

#             for s in area.spaces:
#                 if s.type == 'TEXT_EDITOR':
#                     filenames.add(s.text.name)
#     return filenames


def upload(gist_files_dict, project_name, public_switch):

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
        print(json_to_parse)

        print('received response from server')
        found_json = json_to_parse.readall().decode()
        get_gist_url(found_json)

    upload_gist()


# Gists can contain multiple files, we'll downlaod all by default.

def to_gist(file_names, project_name='noname', public_switch=True):
    gist_files_dict = {}
    for f in file_names:
        tfile = bpy.data.texts.get(f)
        if tfile:
            file_content = tfile.as_string()
            gist_files_dict[f] = {"content": file_content}

    upload(gist_files_dict, project_name, public_switch)


# Gists can contain multiple files, we'll downlaod all by default.

def download(gist_id):

    has_readall = False

    def get_raw_urls_from_gist_id(gist_id):

        gist_id = str(gist_id)
        url = 'https://api.github.com/gists/' + gist_id

        obtained_url = urlopen(url)
        if hasattr(obtained_url, 'readall'):
            found_json = obtained_url.readall().decode()
            has_readall = True
        else:
            found_json = obtained_url.read().decode()

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
        if has_readall:
            content = urlopen(url).readall().decode()
        else:
            content = urlopen(url).read().decode()
        t.from_string(content)

# download('922e5378c1ff87399f62')
