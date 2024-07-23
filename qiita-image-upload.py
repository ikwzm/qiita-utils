#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
import mimetypes
import argparse
import time

class QiitaImageUploader:

    TOKEN_FILE = ".qiita_token"        
    
    def __init__(self, debug_mode=0):
        self.token = self.load_token()
        self.debug = debug_mode
        if self.token == None:
            sys.exit("Not Found Access Token")

    def load_token(self):
        token_file_name = os.path.join(os.getcwd(), self.TOKEN_FILE)
        if os.access(token_file_name, os.R_OK):
            with open(token_file_name, "r") as token_file:
                return token_file.read().strip()

        script_path     = os.path.abspath(__file__)
        script_dir      = os.path.dirname(script_path)
        token_file_name = os.path.join(script_dir, self.TOKEN_FILE)
        if os.access(token_file_name, os.R_OK):
            with open(token_file_name, "r") as token_file:
                return token_file.read().strip()
        return None

    def upload(self, image_name, file_name, image_type):
        if self.debug > 0:
            print(image_name, file_name, image_type)
        with open(file_name, "rb") as image_file:
            image_data = image_file.read()
        image_size = len(image_data)
        headers = {
            "Content-Type":  "application/json",
            "authorization": 'Bearer %s' % (self.token),
        }
        data = {"image": {
            "content_type":  image_type,
            "name":          image_name,
            "size":          image_size,
        }}
        if self.debug > 1:
            print("================ qiita request")
            print(headers)
            print(json.dumps(data))
        qiita_resp = requests.post(
            "https://qiita.com/api/upload/policies",
            data = json.dumps(data),
            headers = headers,
        )
        assert qiita_resp.status_code == 200
        content = qiita_resp.content
        qiita_resp.close()
        qiita_info = json.loads(content.decode())
        if self.debug > 1:
            print("================ qiita_info")
            print(qiita_info)

        upload_url  = qiita_info["upload_url"]
        upload_form = qiita_info["form"]
        if self.debug > 1:
            print("---------------- upload_form")
            print(upload_form)
        ## for name, value in upload_form.items():
        ##     upload_files[name] = (None, value)
        upload_files = {'file': (image_name, image_data, image_type)}
        ## time.sleep(5) ## wait 5sec
        for try_count in range(10):
            if self.debug > 1:
                print("---------------- upload post")
            upload_resp  = requests.post(upload_url, data = upload_form, files = upload_files)
            if self.debug > 1:
                print("---------------- upload resp code")
                print(upload_resp.status_code)
            upload_headers = upload_resp.headers
            upload_content = upload_resp.content
            upload_resp.close()
            if self.debug > 1:
                print (upload_headers)
                print (upload_content)
            if "Location" in upload_headers:
                return upload_headers["Location"]
            time.sleep(1) ## wait 1sec
        return None

if __name__  == "__main__":
    parser = argparse.ArgumentParser(description='Qiita Image Uploader')
    parser.add_argument('file_name'     , help='Image File Name')
    parser.add_argument('-N', '--name'  , help='Image Name'  , action='store', type=str)
    parser.add_argument('-T', '--type'  , help='Image Type'  , action='store', type=str)
    parser.add_argument('-d', '--debug' , help='debug mode ' , action='store', type=int, default=0 )
    args = parser.parse_args()

    file_name = args.file_name
    if args.name == None:
        image_name = os.path.splitext(os.path.basename(file_name))[0]
    else:
        image_name = args.name

    if args.type == None:
        image_type = mimetypes.guess_type(file_name)[0]
    else:
        image_type = args.type

    uploader = QiitaImageUploader(debug_mode=args.debug)
    loc = uploader.upload(image_name, file_name, image_type)
    if loc == None:
        sys.exit("Upload Error %s" % (file_name))
    print(loc)
