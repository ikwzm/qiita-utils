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
            print("## upload: ")
            print("##   image_name:  ", end=""); print(image_name)
            print("##   file_name:   ", end=""); print(file_name)
            print("##   image_type:  ", end=""); print(image_type)
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
            print("## qiita_request: ")
            print("##   header:      ", end=""); print(headers)
            print("##   data:        ", end=""); print(json.dumps(data))
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
            print("## qiita_info:    ", end=""); print(qiita_info)

        upload_url  = qiita_info["upload_url"]
        upload_form = qiita_info["form"]
        if self.debug > 1:
            print("##   url     :    ", end=""); print(upload_url)
            print("##   form:        ", end=""); print(upload_form)
        ## for name, value in upload_form.items():
        ##     upload_files[name] = (None, value)
        upload_files = {'file': (image_name, image_data, image_type)}
        ## time.sleep(5) ## wait 5sec
        for try_count in range(10):
            if self.debug > 1:
                print("## - upload_post: ")
            upload_resp  = requests.post(upload_url, data = upload_form, files = upload_files)
            if self.debug > 1:
                print("##     resp_code: ", end=""); print(upload_resp.status_code)
            upload_headers = upload_resp.headers
            upload_content = upload_resp.content
            upload_resp.close()
            if self.debug > 1:
                print("##     headers:   ", end=""); print(upload_headers)
                print("##     content:   ", end=""); print(upload_content)
            if "Location" in upload_headers:
                image_info = {"name":      image_name,
                              "type":      image_type,
                              "file_name": file_name,
                              "url":      upload_headers["Location"]
                }
                return image_info
            time.sleep(1) ## wait 1sec
        return None

if __name__  == "__main__":
    parser = argparse.ArgumentParser(description='Qiita Image Uploader')
    parser.add_argument('file_name'     , help='Image File Name')
    parser.add_argument('-N', '--name'  , help='Image Name'            , action='store', type=str)
    parser.add_argument('-T', '--type'  , help='Image Type'            , action='store', type=str)
    parser.add_argument('-d', '--debug' , help='debug mode '           , action='store', type=int, default=0 )
    parser.add_argument('--json'        , help='Output result in json' , action='store_true')
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

    uploader   = QiitaImageUploader(debug_mode=args.debug)
    image_info = uploader.upload(image_name, file_name, image_type)
    if image_info == None:
        sys.exit("Upload Error %s" % (file_name))
    if args.json == True:
        print(json.dumps(image_info))
    else:
        print(image_info["url"])
